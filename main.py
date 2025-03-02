# main.py

from flask import Flask, jsonify, Response, request
from helper import load_data, filter_and_paginate
import pandas as pd

app = Flask(__name__)

# Load DataFrame at startup
df = load_data()

@app.route('/')
def home():
    return "Flask API is running. Go to /data to view the CSV in JSON format. "

@app.route('/data', methods=['GET'])
def get_data():
    """Returns the CSV data in JSON or CSV format with filtering and pagination"""
    if df.empty:
        return jsonify({"error": "Failed to load the CSV file"}), 500

    # Validates query parameters for offset and limit
    try:
        limit = int(request.args.get("limit", 10))
        offset = int(request.args.get("offset", 0))

        if limit < 1 or offset < 0:
            raise ValueError("Limit must be greater than 0 and offset cannot be negative.")
    except ValueError:
        return jsonify({
            "error": "'limit' and 'offset' must be positive."}), 400
    
    # Validates arguments. Essentially spellchecking    
    for key, value in request.args.items():
        if key not in df.columns and key not in ["limit", "offset", "format"]:
            return jsonify({"error": f"Invalid filter key: '{key}' is not a valid column."}), 400

        # Check if the filter value is valid for Country
        if key == "Country" and value not in df["Country"].unique():
            return jsonify({"error": f"Invalid country name: '{value}' is not in the dataset."}), 400

    # Try to apply filters and pagination
    try:
        paginated_df, output_format = filter_and_paginate(df, request.args)

        #Checking if df is empty
        if paginated_df.empty:
            return jsonify({"error": "No data found."}), 404

    # Generic server error check
    except Exception as e:
        return jsonify({"error": f"An error occurred while processing data: {str(e)}"}), 500


    # Return CSV if requested
    if output_format == "csv":
        return Response(
            paginated_df.to_csv(index=False),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=data.csv"},
        )

    # Otherwise, return JSON
    return jsonify(paginated_df.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)