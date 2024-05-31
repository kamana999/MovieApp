import os
import logging
import pandas as pd
from bson.objectid import ObjectId
from datetime import datetime

from . import celery
from app.database import SessionManager, Collections
from app.utils.const import csv_headers, pd_chunk_size

logger = logging.getLogger(__name__)


@celery.task()
def process_csv(file_id):
    """
    Celery task to process a CSV file.

    Args:
        file_id (str): The ObjectId of the file to be processed.

    Returns:
        None
    """
    # Open a session to the database
    with SessionManager() as (client, db):
        # Retrieve the file from the database
        csv_files_collection = db.get_collection(Collections.csv_files)
        file = csv_files_collection.find_one({'_id': ObjectId(file_id)})
        
        # If the file exists
        if file:
            try:
                # Get the file path
                file_path = file['filepath']
                
                # If the file exists
                if os.path.exists(file_path):
                    # Update the file status in the database
                    csv_files_collection.update_one(
                        {'_id': file['_id']}, 
                        {'$set': {'status': 'in_progress', 'updated_at': datetime.now()}}
                    )
                    
                    # Read the CSV file in chunks
                    chunk = pd.read_csv(file_path, chunksize=pd_chunk_size)
                    movies_collection = db.get_collection(Collections.movies)
                    success = True
                    processed = 0
                    
                    # Iterate over the chunks
                    for i, df in enumerate(chunk):
                        # Validate the header on the first chunk
                        if i == 0:
                            if df.columns.tolist() != csv_headers:
                                success = False
                                logger.info('Invalid header')
                                # Update the file status in the database
                                csv_files_collection.update_one(
                                    {'_id': file['_id']}, 
                                    {'$set': {'status': 'failed', 
                                            'error': 'Invalid header', 
                                            'processed_at': datetime.now(), 
                                            'updated_at': datetime.now()}}
                                )
                                break
                        
                        # Add additional columns to the DataFrame
                        df['created_at'] = datetime.now()
                        df['updated_at'] = datetime.now()
                        df['created_by'] = file['uploaded_by']
                        df['sourced_from'] = file['_id']

                        # Replace null values with empty strings
                        df = df.fillna('')

                        # Convert DataFrame to list of dictionaries
                        data = df.to_dict('records')
                        
                        # Insert the data into the movies collection
                        movies_collection.insert_many(data)
                        
                        # Update the progress
                        processed += len(data)
                        logger.info('Progress: {}'.format(processed))
                        
                        # Update the file status in the database
                        csv_files_collection.update_one(
                            {'_id': file['_id']}, 
                            {'$set': {'progress': processed, 'updated_at': datetime.now()}}
                        )

                    # If the file was processed successfully
                    if success:
                        # Update the file status in the database
                        csv_files_collection.update_one(
                            {'_id': file['_id']}, 
                            {'$set': {'status': 'processed', 
                                    'processed_at': datetime.now(), 
                                    'updated_at': datetime.now()}}
                        )
                        logger.info('File processed successfully: {}'.format(file_path))    
                else:
                    logger.info('File not found')
                    # Update the file status in the database
                    csv_files_collection.update_one(
                        {'_id': file['_id']}, 
                        {'$set': {'status': 'failed', 
                                'error': 'File not found',
                                'processed_at': datetime.now(),
                                'updated_at': datetime.now()}}
                    )
            except Exception as e:
                logger.info(e)
                # Update the file status in the database
                csv_files_collection.update_one(
                    {'_id': file['_id']}, 
                    {'$set': {'status': 'failed', 
                            'error': str(e), 
                            'processed_at': datetime.now(), 
                            'updated_at': datetime.now()}}
                )     
        else:
            logger.info('File not found')
