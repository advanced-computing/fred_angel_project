from flask import Flask, jsonify, Response
import pandas as pd
import requests
import json
from io import StringIO

app = Flask(__name__)

# URL del archivo CSV en GitHub en formato RAW
CSV_URL = "https://raw.githubusercontent.com/advanced-computing/fred_angel_project/main/un_data.csv"

# Cargar los datos con Pandas desde GitHub
response = requests.get(CSV_URL)

if response.status_code == 200:
    df = pd.read_csv(StringIO(response.text), encoding="latin1")
else:
    df = pd.DataFrame()  # Crea un DataFrame vacío si hay error
    print("Error al cargar el archivo CSV desde GitHub")

@app.route('/')
def home():
    return "Flask API funcionando. Ve a /data para ver el CSV en formato JSON."

@app.route('/data', methods=['GET'])
def get_data():
    """ Devuelve los datos del CSV en formato JSON con indentación """
    json_data = json.dumps(df.to_dict(orient="records"), indent=2, ensure_ascii=False)
    return Response(json_data, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
