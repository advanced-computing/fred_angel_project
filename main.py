from flask import Flask, jsonify, Response, request
from error_handling import handle_no_results, handle_server_error
from validate import validate_all_filters
from helper import initialize_database, filter_and_paginate, get_valid_countries, add_user

app = Flask(__name__)

initialize_database()

@app.route('/')
def home():
    return "Flask API is running. Go to /data to view the database in JSON format."

@app.route('/data', methods=['GET'])
def get_data():
    valid_countries = get_valid_countries()
    
    filters = validate_all_filters(request.args, valid_countries)
    
    if isinstance(filters, tuple):
        return filters

    try:
        result_df = filter_and_paginate(request.args)
        if result_df.empty:
            return handle_no_results()
    except Exception as e:
        return handle_server_error(e)

    if request.args.get("format", "").lower() == "csv":
        return Response(
            result_df.to_csv(index=False),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=data.csv"},
        )

    return jsonify(result_df.to_dict(orient="records"))

@app.route('/users', methods=['POST'])
def add_user_endpoint():
    data = request.get_json()
    # Validate that the required fields are provided
    if not data or not all(k in data for k in ('username', 'age', 'country')):
        return jsonify({'error': 'Missing required fields: username, age, country'}), 400

    result = add_user(data['username'], data['age'], data['country'])
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)