# This is relatively simple, but in the interest in making everything modular
#       here is the seperate file.

from flask import jsonify



def handle_invalid_parameters():
    """Handles invalid 'limit' and 'offset' query parameters."""
    return jsonify({"error": "'limit' and 'offset' must be positive."}), 400

def handle_invalid_filter_key(key):
    """Handles errors when an invalid filter column is used."""
    return jsonify({"error": f"Invalid filter key: '{key}' is not a valid column."}), 400

def handle_invalid_country(value):
    """Handles errors when an invalid country name is used."""
    return jsonify({"error": f"Invalid country name: '{value}' is not in the dataset."}), 400

def handle_no_results():
    """Handles cases where filters return an empty DataFrame."""
    return jsonify({"error": "No data found."}), 404

def handle_server_error(error):
    """Handles unexpected server errors."""
    return jsonify({"error": f"An error occurred while processing data: {str(error)}"}), 500
