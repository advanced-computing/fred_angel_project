# main.py

from flask import Flask, jsonify, Response, request
from helper import load_data, filter_and_paginate
from error_handling import handle_no_results, handle_server_error
from validate import validate_limit_offset, validate_filter_keys, validate_country


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
    valid, result = validate_limit_offset(request.args)
    if not valid:
        return result
    limit, offset = result
    
    # Validates arguments. Essentially spellchecking    
    valid, result = validate_filter_keys(request.args)
    if not valid:
        return result

    # Checks if the value is valid for Country (does it exist in df)
    valid, result, status = validate_country(request.args, df["Country"].unique())
    if not valid:
        return result
 
    # Apply filters and pagination
    try:
        paginated_df, output_format = filter_and_paginate(df, request.args)

        # Checks if df is empty after filter/paginated
        if paginated_df.empty:
            return handle_no_results()

    # Generic server error check
    except Exception as e:
        return handle_server_error(e)


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