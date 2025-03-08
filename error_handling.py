from flask import jsonify

def handle_bad_request(message):
    return jsonify({"error": message}), 400

def handle_invalid_parameters():
    return jsonify({"error": "'limit' and 'offset' must be positive integers."}), 400

def handle_invalid_filter_key(key):
    return jsonify({"error": f"Invalid filter key: '{key}' is not a valid column in the dataset."}), 400

def handle_invalid_country(value):
    return jsonify({"error": f"Invalid country name: '{value}' does not exist in the dataset."}), 400

def handle_no_results():
    return jsonify({"error": "No data found with the given filters."}), 404

def handle_server_error(error):
    return jsonify({"error": f"An error occurred while processing data: {str(error)}"}), 500