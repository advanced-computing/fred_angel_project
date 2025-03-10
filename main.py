from flask import Flask, jsonify, Response, request
from error_handling import handle_no_results, handle_server_error
from validate import validate_all_filters
from helper import initialize_database, filter_and_paginate, get_valid_countries

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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)