import logging

from app.database import SessionManager, Collections
from app.utils.auth import hash_password

logger = logging.getLogger(__name__)


def load_bootstrap_data():
    """
    Function to load initial bootstrap data into the database.

    This function creates a new user with the username 'admin' and
    password 'admin' if one does not already exist in the database.
    """
    # User credentials
    user = {
        'username': 'admin',  # Default username
        'password': 'admin'  # Default password
    }

    with SessionManager() as (client, db):
        # Log the creation of the admin user
        logger.info('creating admin user')

        # Hash the user's password
        user['password'] = hash_password(user['password'])

        # Get the users collection
        users = db.get_collection(Collections.users)

        # Check if the user already exists
        if users.find_one({'username': user['username']}):
            # Log if the user already exists
            logger.info('user already exists')
        else:
            # Insert the new user into the database
            users.insert_one(user)

        # Log the completion of the data loading
        logger.info('done')
