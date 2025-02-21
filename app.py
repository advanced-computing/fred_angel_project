from flask import Flask, jsonify, Response
import pandas as pd
import requests
import json
from io import StringIO

app = Flask(__name__)

# URL del archivo CSV en GitHub en formato RAW
CSV_URL = "https://raw.githubusercontent.com/advanced-computing/fred_angel_project/main/un_data.csv"


def load_data():
    '''
 Load and format CSV into a Pandas dataframe
     '''
        
    response = requests.get(CSV_URL)
    data = pd.read_csv(StringIO(response.text), encoding="ISO-8859-1", skiprows=1, header=0)

    # Rename columns for clarity
    data = data.rename(columns={
            "Region/Country/Area": "Region Code", "Unnamed: 1": "Region"})

    return data

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
    if df.empty:
        return "No me culpa, fue Angel"

    return df.to_json(orient="records")

if __name__ == '__main__':
    app.run(debug=True)
