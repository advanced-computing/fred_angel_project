from flask import Flask, jsonify, request
import pandas as pd
import requests
import io

app = Flask(__name__)

# URL del archivo CSV en GitHub (versión cruda)
CSV_URL = "https://raw.githubusercontent.com/advanced-computing/fred_angel_project/main/un_data.csv"

def load_data():
    """Descargar y cargar el CSV desde GitHub."""
    response = requests.get(CSV_URL)
    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.text), encoding='latin1')

        # Renombrar columnas
        df = df.rename(columns={
            "T02": "Region_ID",
            "Population, density and surface area": "Country_Area",
            "Unnamed: 2": "Year",
            "Unnamed: 3": "Series",
            "Unnamed: 4": "Value",
            "Unnamed: 5": "Footnotes",
            "Unnamed: 6": "Source"
        })

        # Eliminar filas innecesarias
        df = df.iloc[1:].reset_index(drop=True)

        # Convertir columnas a tipos adecuados
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
        df["Value"] = pd.to_numeric(df["Value"].str.replace(",", ""), errors="coerce")

        return df
    else:
        return None

df = load_data()

@app.route("/")
def hello_world():
    """Return a friendly HTTP greeting."""
    return "<p>Hello, World! Welcome to the UN Data API.</p>"

@app.route("/records", methods=["GET"])
def list_records():
    """Return a list of records with optional filtering and pagination."""
    if df is None:
        return jsonify({"error": "Error loading data from GitHub"}), 500

    # Parámetros de filtrado y paginación
    limit = request.args.get("limit", default=10, type=int)
    offset = request.args.get("offset", default=0, type=int)

    # Filtrar datos por cualquier columna pasada como parámetro
    filters = {k: v for k, v in request.args.items() if k not in ['limit', 'offset']}

    filtered_df = df
    for key, value in filters.items():
        if key in df.columns:
            filtered_df = filtered_df[filtered_df[key].astype(str) == value]

    paginated_df = filtered_df.iloc[offset:offset+limit]

    return jsonify(paginated_df.to_dict(orient="records"))

@app.route("/records/<region_id>/<year>", methods=["GET"])
def get_record(region_id, year):
    """Retrieve a single record by Region_ID and Year."""
    if df is None:
        return jsonify({"error": "Error loading data from GitHub"}), 500

    record = df[(df["Region_ID"].astype(str) == region_id) & (df["Year"].astype(str) == year)]

    if record.empty:
        return jsonify({"error": "Record not found"}), 404

    return jsonify(record.to_dict(orient="records"))

@app.route("/sum", methods=["GET"])
def sum_numbers():
    """Return the sum of two numbers."""
    a = request.args.get("a")
    b = request.args.get("b")

    if a is None or b is None:
        return jsonify({"error": "Please provide both 'a' and 'b' parameters"}), 400

    try:
        result = int(a) + int(b)
    except ValueError:
        return jsonify({"error": "Invalid input, please enter integers"}), 400

    return jsonify({"sum": result})

def factorial(n):
    """Calculate the factorial of a number."""
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

@app.route("/factorial", methods=["GET"])
def factorial_route():
    """Return the factorial of a number."""
    n = request.args.get("n", 10)

    try:
        result = factorial(int(n))
    except ValueError:
        return jsonify({"error": "Invalid number"}), 400

    return jsonify({"number": n, "factorial": result})

if __name__ == "__main__":
    app.run(debug=True, port=5050)  # Se cambia el puerto a 5050
