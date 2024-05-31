from flask import Blueprint, request, jsonify, make_response
from app.database import SessionManager, Collections
from app.utils.auth import generate_token
from app.utils.auth import verify_password

user_router = Blueprint('api', __name__)


@user_router.route('/login', methods=['POST'])
def login():
    """
    Endpoint for user login.
    Expects a JSON payload with 'username' and 'password' fields.
    Returns a token if credentials are valid.
    """
    # Get the JSON payload
    data = request.get_json()

    # Extract username and password from the payload
    username = data.get('username')
    password = data.get('password')

    # Check if both fields are present
    if not username or not password:
        # Return an error if either field is missing
        return make_response('Username and password are required', 400)

    # Use SessionManager to get a database connection
    with SessionManager() as (client, db):
        # Get the users collection
        users = db.get_collection(Collections.users)

        # Find the user with the given username
        user = users.find_one({'username': username})

        # Check if the user exists
        if not user:
            # Return an error if the user does not exist
            return make_response(jsonify({"message": "Invalid username or password"}), 401)

        # Get the stored password for the user
        stored_password = user.get('password')

        # Check if the stored password is valid
        if stored_password and verify_password(password, stored_password):
            # Generate a token for the user
            token = generate_token(user)

            # Prepare the response data
            res_data = {
                'username': username,
                'token': token,
                'message': 'Login successful'
            }

            # Return the token and success message
            return make_response(jsonify(res_data), 200)

    # Return an error if the credentials are invalid
    return make_response(jsonify({"message": "Invalid username or password"}), 401)
