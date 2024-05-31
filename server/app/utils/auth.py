import os
import logging
import bcrypt

from functools import wraps
from jwt import PyJWTError, decode, encode
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from flask import request, jsonify

from app.database import SessionManager, Collections

logger = logging.getLogger(__name__)


# validate token decorator
def jwt_required(f):
    """
    Decorator that validates JWT token in the Authorization header.

    Args:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        """
        Decorated function that validates JWT token and calls the decorated function with the user object.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Flask response: The response returned by the decorated function.
        """
        # Get the authorization header from the request
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                # Extract the token from the authorization header
                token = auth_header.split()[1]
                # Decode the token and get the payload
                payload = decode(token, os.environ.get('JWT_SECRET_KEY'), algorithms=['HS256'])
                # Check if the token has expired
                if datetime.now() > datetime.fromtimestamp(payload['exp']):
                    return jsonify({'error': 'Token has expired'}), 401
                else:
                    with SessionManager() as (client, db):
                        # Get the users collection
                        users = db.get_collection(Collections.users)
                        # Find the user with the given id in the payload
                        user = users.find_one({'_id': ObjectId(payload['sub'])})
                        # Check if the user exists
                        if not user:
                            return jsonify({'error': 'Invalid token'}), 401
                        # Call the decorated function with the user object
                        return f(user, *args, **kwargs)
            except PyJWTError:
                return jsonify({'error': 'Invalid token'}), 401
        else:
            # Return an error if the token is missing
            return jsonify({'error': 'Missing token'}), 401

    return decorated


# generate token function
def generate_token(user):
    """
    Generates a JWT token for the given user.

    Args:
        user (dict): A dictionary representing the user.

    Returns:
        str: The generated JWT token.
    """
    # Generate the payload for the token
    payload = {
        'sub': str(user.get('_id')),  # Subject: user id
        'iat': datetime.now(),  # Issued at: current timestamp
        'exp': datetime.now() + timedelta(days=1)  # Expiration: 1 day from now
    }

    # Encode the payload into a JWT token using the secret key
    token = encode(payload, os.environ.get('JWT_SECRET_KEY'), algorithm='HS256')

    return token


def hash_password(password):
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.
    """
    # Encode the password as bytes and generate a salt
    encoded_password = password.encode('utf-8')
    salt = bcrypt.gensalt()

    # Hash the encoded password with the salt
    hashed_password = bcrypt.hashpw(encoded_password, salt)

    return hashed_password


def verify_password(password, hashed_password):
    """
    Verifies if a password matches a hashed password using bcrypt.

    Args:
        password (str): The password to be verified.
        hashed_password (bytes): The hashed password to compare against.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    # Encode the password as bytes and try to verify it with the hashed password
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    # If there's an exception, log the error and return False
    except Exception as e:
        logger.error(e)
        return False
