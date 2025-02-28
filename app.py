from flask import Flask, jsonify, Response, request
from helper import load_data, filter_and_paginate
import pandas as pd

app = Flask(__name__)

# Load DataFrame at startup
df = load_data()

@app.route('/')
def home():
    return "Flask API is running. Go to /data to view the CSV in JSON format."

@app.route('/data', methods=['GET'])
def get_data():
    """Returns the CSV data in JSON or CSV format with filtering and pagination"""
    if df.empty:
        return jsonify({"error": "Failed to load the CSV file"}), 500

    # Filter and paginate the DataFrame
    paginated_df, output_format = filter_and_paginate(df, request.args)

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