from flask import Flask, jsonify, Response, request
import pandas as pd
import requests
from io import StringIO

app = Flask(__name__)

# URL of the CSV file on GitHub (RAW format)
CSV_URL = "https://raw.githubusercontent.com/advanced-computing/fred_angel_project/main/un_data.csv"

def load_data():
    '''
    Load and format CSV into a Pandas DataFrame
    '''
    response = requests.get(CSV_URL)
    if response.status_code == 200:
        data = pd.read_csv(StringIO(response.text), encoding="ISO-8859-1", skiprows=1, header=0)
        # Rename columns for clarity
        data = data.rename(columns={"Region/Country/Area": "Region Code", "Unnamed: 1": "Country"})
        return data
    else:
        print("Error loading the CSV file from GitHub")
        return pd.DataFrame()  # Create an empty DataFrame if there's an error

df = load_data()

@app.route('/')
def home():
    return "Flask API is running. Go to /data to view the CSV in JSON format."

@app.route('/data', methods=['GET'])
def get_data():
    """ Returns the CSV data in JSON or CSV format with filtering and pagination """
    if df.empty:
        return jsonify({"error": "Failed to load the CSV file"}), 500

    # Filtering and pagination parameters
    limit = request.args.get("limit", default=10, type=int)
    offset = request.args.get("offset", default=0, type=int)
    output_format = request.args.get("format", default="json")
    
    filters = {k: v for k, v in request.args.items() if k not in ['limit', 'offset', 'format']}
    filtered_df = df
    for key, value in filters.items():
        if key in df.columns:
            filtered_df = filtered_df[filtered_df[key].astype(str) == value]

    paginated_df = filtered_df.iloc[offset:offset+limit]

    if output_format == "csv":
        return Response(paginated_df.to_csv(index=False), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=data.csv"})
    
    return jsonify(paginated_df.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(debug=True)
