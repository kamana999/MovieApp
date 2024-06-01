import os
import logging

from bson.objectid import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from flask import Blueprint, jsonify, request

from app.celery import celery
from app.utils.auth import jwt_required
from app.utils.file_handler import format_file_name
from app.database import SessionManager, Collections
from app.utils.helper import paginator

logger = logging.getLogger(__name__)

csv_router = Blueprint('upload', __name__)


@csv_router.route('/upload', methods=['POST'])
@jwt_required
def upload_csv(user, *args, **kwargs):
    """
    Uploads a CSV file and saves it to the database.

    Args:
        user (dict): The user making the request.

    Returns:
        A JSON response with a success message and the uploaded file details
        if the file is uploaded successfully. If there is an error, returns a
        JSON response with an error message and an HTTP status code.
    """
    # Check if a file was provided in the request
    if 'file' not in request.files:
        logger.info(f"No file part in the request.")
        return {'error': 'No file part'}, 400

    try:
        # Get the file from the request
        file = request.files['file']

        # Check if a file was selected
        if file.filename == '':
            return {'message': 'No selected file'}, 400

        # Check if the file is a CSV file
        if file and file.filename.endswith('.csv'):
            chunk_size = 4096
            filename = format_file_name(file.filename)
            file_path = f'/app/data/{filename}'
            logger.info(f'File path: {file_path}')

            # Save the file to the server
            with open(file_path, 'wb') as f:
                logger.info(f'Saving file: {f.name}')
                while True:
                    chunk = file.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)

                logger.info(f'File uploaded successfully: {f.name}')

            # Save the file details to the database
            with SessionManager() as (client, db):
                csv_files = db.get_collection(Collections.csv_files)
                file_dict = {
                    'filepath': file_path,
                    'filename': filename,
                    'status': 'pending',
                    'processed_at': None,
                    'uploaded_by': user.get('_id'),
                    'created_at': datetime.now(),
                    'updated_at': datetime.now(),
                    'file_size': os.path.getsize(file_path),
                    'progress': 0
                }
                file_obj = csv_files.insert_one(file_dict)
                file_dict['_id'] = str(file_obj.inserted_id)
                file_dict['uploaded_by'] = str(file_dict['uploaded_by'])
                celery.send_task('app.celery.tasks.process_csv',
                                args=[str(file_obj.inserted_id)])

            return {'message': 'File uploaded successfully',
                    'data': file_dict}, 200

        return {'error': 'Invalid file format'}, 400
    except Exception as e:
        return {'error': str(e)}, 500


@csv_router.route('/list/', methods=['GET'])
@jwt_required
def get_file_list(user, *args, **kwargs):
    """
    Retrieves a paginated list of CSV files from the database.

    Args:
        user (dict): The user making the request.

    Returns:
        flask.Response: A JSON response containing the list of CSV files.
    """
    rqst_args = request.args  # Get the request arguments
    logger.info(rqst_args)  # Log the request arguments

    with SessionManager() as (client, db):
        csv_files_collection = db.get_collection(Collections.csv_files)  # Get the CSV files collection

        search_allowed_fields = {'filename': 1, 'status': 1}  # Fields allowed for searching
        sort_allowed_fields = {'_id': -1, 'created_at': -1, 'updated_at': -1}  # Fields allowed for sorting

        # Retrieve the paginated data
        data = paginator(csv_files_collection, rqst_args, search_allowed_fields, sort_allowed_fields)

        file_list = data['data']  # Get the list of files

        # Transform the file list to include the necessary fields and convert the IDs to strings
        transformed_file_list = [{
            **x, '_id': str(x['_id']),
            'uploaded_by': str(x['uploaded_by']),
        } for x in file_list]

        # Construct the response
        return jsonify({
            'total_count': data['total_count'],
            'data': transformed_file_list,
            'page': data['page'],
            'page_size': data['page_size'],
            'skip': data['skip']
        })


@csv_router.route('/get/<file_id>', methods=['GET'])
@jwt_required
def get_file_by_id(user, file_id, *args, **kwargs):
    """
    Get a file by its ID.

    Args:
        user (str): The user making the request.
        file_id (str): The ID of the file to retrieve.

    Returns:
        dict: A JSON representation of the file, or an empty JSON object with a 404 status code if the file is not found.
    """
    with SessionManager() as (client, db):
        try:
            # Get the CSV files collection
            csv_file_collection = db.get_collection(Collections.csv_files)

            # Find the file by its ID
            file = csv_file_collection.find_one({'_id': ObjectId(file_id)})

            # If the file is found, return it as a JSON object
            if file:
                return jsonify({**file, '_id': str(file['_id']), 'uploaded_by': str(file['uploaded_by'])})

            # If the file is not found, log a message and return an empty JSON object with a 404 status code
            logger.info('file not found')
            return jsonify({}), 404
        except InvalidId:
            # If the file ID is invalid, log an error and return an empty JSON object with a 404 status code
            logger.error('Invalid ID')
            return jsonify({}), 404
