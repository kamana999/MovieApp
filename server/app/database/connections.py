import os
import logging

from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mongo_uri = os.environ.get('MONGO_URI')


class Collections(object):
    users = 'users'
    csv_files = 'csv_files'
    movies = 'movies'


class SessionManager:

    def __init__(self):
        """
        Initialize a new instance of SessionManager.

        This class is responsible for managing the MongoDB connection
        and provides a context manager interface for using the database.

        Attributes:
            mongo_uri (str): The URI of the MongoDB database.
            client (pymongo.MongoClient): The MongoDB client.
            db (pymongo.database.Database): The MongoDB database.
        """
        # Get the URI of the MongoDB database from the environment variables
        self.mongo_uri = mongo_uri
        
        # Initialize the MongoDB client and database objects
        self.client = None
        self.db = None

    def __enter__(self):
        """
        Context manager method to enter the context.

        Initializes the MongoDB client and database objects,
        and returns the client and database objects.

        Returns:
            tuple: A tuple containing the MongoDB client and database objects.
        """
        # Initialize the MongoDB client
        self.client = MongoClient(self.mongo_uri)
        logger.info('Connected to MongoDB')

        # Get the MongoDB database
        self.db = self.client.get_database()

        # Get the get_collection method from the database object
        self.get_collection = getattr(self.db, 'get_collection')

        # Set the get_collection method in the database object to
        # call the modified get_collection method
        setattr(self.db, 'get_collection', self.get_collection)

        # Return the client and database objects
        return self.client, self.db

    def get_collection(self, collection):
        """
        Get a collection from the database.

        Args:
            collection (str): The name of the collection to get.

        Raises:
            Exception: If the collection does not exist.

        Returns:
            pymongo.collection.Collection: The requested collection.
        """
        # Check if the collection exists in the Collections class
        if collection not in Collections.__dict__.values():
            # Log the error and raise an exception if the collection does not exist
            logger.error('invalid collection')
            raise Exception('Collection does not exist')

        # Return the requested collection
        return self.get_collection(collection)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager and close the MongoDB client.

        Args:
            exc_type: The type of the exception.
            exc_val: The exception value.
            exc_tb: The exception traceback.

        Returns:
            None
        """
        # Close the MongoDB client
        self.client.close()
        
        # Log the disconnection message
        logger.info('Disconnected from MongoDB')
