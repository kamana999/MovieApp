import re
import uuid


def format_file_name(file_name):
    """
    Formats a file name by removing special characters and spaces,
    adding a unique substring at the end, and returning the formatted file name.

    Args:
        file_name (str): The original file name.

    Returns:
        str: The formatted file name.
    """
    # Split the file name into name and extension
    filename_split = file_name.split('.')
    file_name, file_extension = filename_split[0], filename_split[-1]

    # Remove special characters and spaces
    file_name = re.sub(r'[^\w\s-]', '', file_name)  # Remove all non-alphanumeric, non-space, non-hyphen characters
    file_name = re.sub(r'\s+', '-', file_name)  # Replace consecutive spaces with a single hyphen

    # Add a unique substring at the end
    unique_substring = str(uuid.uuid4())[:8]  # Generate a unique substring from the first 8 characters of a UUID
    formatted_file_name = f"{file_name}-{unique_substring}.{file_extension}"  # Construct the formatted file name

    return formatted_file_name
