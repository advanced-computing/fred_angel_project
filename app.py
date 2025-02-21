from flask import Flask, jsonify, request, Response
import pandas as pd
import requests
import io

app = Flask(__name__)

# Load CSV from GitHub
CSV_URL = "https://raw.githubusercontent.com/advanced-computing/fred_angel_project/main/un_data.csv"

def load_data():
    '''
    Loading in the data, 
    '''
    response = requests.get(CSV_URL)
    df = pd.read_csv(io.StringIO(response.text), encoding='latin1')

    df = df.rename(columns={
        "T02": "Region_ID",
        "Population, density and surface area": "Country_Area",
        "Unnamed: 2": "Year",
        "Unnamed: 3": "Series",
        "Unnamed: 4": "Value",
        "Unnamed: 5": "Footnotes",
        "Unnamed: 6": "Source"
    }).iloc[1:].reset_index(drop=True)
    
    return df

df = load_data()

@app.route("/")
def home():
    return "<p>Hi soy Angel, Fujimori para siempre.</p>"

@app.route("/records", methods=["GET"])
def list_records():
    """
    Displays a list of the UN data records. This function 
        can change pagination using limit and output parameters. It can change 
        the file format from json to csv as well using output_format parameter.
    """
    limit = request.args.get("limit", default=10, type=int)
    offset = request.args.get("offset", default=0, type=int)
    output_format = request.args.get("format", default="json")

    # Apply filtering using a loop instead of list comprehension
    filtered_df = df.copy()
    for key, value in request.args.items():
        if key in df.columns and key not in ["limit", "offset", "format"]:
            filtered_df = filtered_df[filtered_df[key] == value]

    paginated_df = filtered_df.iloc[offset:offset + limit]

    if output_format == "csv":
        return Response(paginated_df.to_csv(index=False), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=records.csv"})

    return jsonify(paginated_df.to_dict(orient="records"))

@app.route("/records/<region_id>/<year>", methods=["GET"])
def get_record(region_id, year):
    """
    Retrieve a single record by Region_ID and Year. There is no unique identifier, so
        a composite key is used instead. No country/year combo occurs twice, but multiple
        rows of data are stored for each country/year (similar to a pivot table).
    """
    record = df[(df["Region_ID"] == region_id) & (df["Year"] == year)]

    return jsonify(record.iloc[0].to_dict()) if not record.empty else jsonify({"no record: "}), 404

if __name__ == "__main__":
    app.run(debug=True)
