from .const import default_page_size


def paginator(collection, rqst_args, search_allowed_fields, sort_allowed_fields):
    """
    Paginate the result of a mongo collection based on request arguments.

    Args:
        collection (object): mongo collection
        rqst_args (object): request args
        search_allowed_fields (dict): allowed fields for search
        sort_allowed_fields (dict): allowed fields for sort, -1 for descending, 1 for ascending

    Returns:
        dict: total_count, data, page, page_size, skip
    """
    # Initialize the find context using the search parameters
    # The find context is only used if search_allowed_fields is not empty
    find_context = {}
    if search_allowed_fields:
        # If search_key and search_term are provided and search_key is an allowed search field
        # then add the search term to the find context with a regex search
        search_key = rqst_args.get('search_key')
        search_term = rqst_args.get('search_term')
        if search_key and search_term and search_allowed_fields.get(search_key):
            find_context[search_key] = {'$regex': search_term, '$options': 'i'}

    # Initialize the sort parameter using the sort parameters
    # The sort parameter is set to {'created_at': -1} if sort_allowed_fields is empty
    # or if sort_key is not an allowed sort field
    sort = None
    if sort_allowed_fields:
        sort_key = rqst_args.get('sort_key')
        sort_value = int(rqst_args.get('sort_value', sort_allowed_fields.get(sort_key, 1)))
        if sort_key and sort_value and sort_allowed_fields.get(sort_key):
            sort = {sort_key: sort_value}
        else:
            sort = {'created_at': -1}

    # Initialize the page, page_size, and skip parameters using the request arguments
    page = int(rqst_args.get('page', 1))
    page_size = int(rqst_args.get('page_size', default_page_size))
    skip = (page - 1) * page_size
    if rqst_args.get('total_count', 'false') == 'true':
        total_count = collection.count_documents(find_context)
    else:
        total_count = None

    # Return the total count, data, page, page_size, and skip
    return {
        # Count the number of documents in the collection that match the find context
        'total_count': total_count,
        # Find documents in the collection that match the find context,
        # skip a certain number of documents, limit the result to a certain number of documents,
        # and sort the result based on the sort parameter
        'data': list(collection.find(find_context).skip(skip).limit(page_size).sort(sort)),
        'page': page,
        'page_size': page_size,
        'skip': skip
    }
