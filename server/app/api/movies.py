import logging

from bson.objectid import ObjectId
from bson.errors import InvalidId

from flask import Blueprint, jsonify, request
from app.utils.auth import jwt_required
from app.database import SessionManager, Collections
from app.utils.helper import paginator


logger = logging.getLogger(__name__)
movies_router = Blueprint('movies', __name__)


@movies_router.route('/list/', methods=['GET'])
@jwt_required
def get_movie_list(user, *args, **kwargs):
    """
    Get a list of movies.

    Args:
        user (dict): The user making the request.
        *args: Additional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        flask.Response: A JSON response containing a list of movies.
    """
    # Get request arguments
    rqst_args = request.args

    # Log request arguments
    logger.info(rqst_args)

    # Get the movies collection
    with SessionManager() as (client, db):
        movies_collection = db.get_collection(Collections.movies)

        # Define fields to be used for search
        search_allowed_fields = {'title': 1, 'type': 1, 'director': 1, 'country': 1, 'release_year': 1}

        # Define fields to be used for sorting
        sort_allowed_fields = {'_id': 1, 'show_id': 1,'created_at': 1, 'updated_at': 1, 'release_year':-1, 'duration':-1, 'date_added':-1}

        # Get paginated movie data
        data = paginator(movies_collection, rqst_args, search_allowed_fields, sort_allowed_fields)

        # If movies are found, return their data
        
        movies = data['data']
        return jsonify({
            'total_count': data['total_count'],
            'data': [{
                **movie, '_id': str(movie['_id']),
                'created_by': str(movie['created_by']),
                'sourced_from': str(movie['sourced_from'])
                } for movie in movies],
            'page': data['page'],
            'page_size': data['page_size'],
            'skip': data['skip']
        })

@movies_router.route('/get/<movie_id>', methods=['GET'])
@jwt_required
def get_movies_by_id(user, movie_id, *args, **kwargs):
    """
    Get a movie by its ID.

    Args:
        user (dict): The user making the request.
        movie_id (str): The ID of the movie.

    Returns:
        flask.Response: A JSON response containing the movie data.
    """
    # Convert the movie_id to ObjectId
    try:
        movie_id = ObjectId(movie_id)
    except InvalidId:
        logger.error('Invalid ID')
        return jsonify({}), 404

    # Get the movies collection
    with SessionManager() as (client, db):
        movies_collection = db.get_collection(Collections.movies)

        # Find the movie by its ID
        movie = movies_collection.find_one({'_id': movie_id})

        # If the movie is found, return its data
        if movie:
            return jsonify({
                **movie,
                '_id': str(movie['_id']),
                'created_by': str(movie['created_by']),
                'sourced_from': str(movie['sourced_from'])
            })

        # If the movie is not found, log a message and return a 404 response
        logger.info('Movie not found')
        return jsonify({}), 404
