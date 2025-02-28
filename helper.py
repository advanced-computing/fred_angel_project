# helper.py

import pandas as pd
import requests
from io import StringIO

# URL of the CSV file on GitHub (RAW format)
CSV_URL = "https://raw.githubusercontent.com/advanced-computing/fred_angel_project/main/un_data.csv"

def load_data():
    """
    Loads the UN data, cleans and renames columns
    Returns a dataframe
    """
    response = requests.get(CSV_URL)
    if response.status_code == 200:
        df = pd.read_csv(StringIO(response.text), encoding="ISO-8859-1", skiprows=1, header=0)
        # Rename columns for clarity
        df = df.rename(columns={"Region/Country/Area": "Region Code", "Unnamed: 1": "Country"})
        return df
    else:
        print("Error loading the CSV file from GitHub")
        return pd.DataFrame()  # Return an empty DataFrame if there's an error

def filter_and_paginate(dataframe, params):
    """
    Allows user to filter and paginate using parameters.
    Parameter options: 'limit' (), 'offset', and 'format' 
    Can pass column names as well (Need to add)
    """
    # Extract pagination parameters
    limit = int(params.get("limit", 10))
    offset = int(params.get("offset", 0))
    output_format = params.get("format", "json")

    # Build filters from remaining parameters
    filters = {k: v for k, v in params.items() if k not in ['limit', 'offset', 'format']}

    # Apply filters
    filtered_df = dataframe
    for key, value in filters.items():
        if key in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[key].astype(str) == value]

    # Pagination
    paginated_df = filtered_df.iloc[offset : offset + limit]

    return paginated_df, output_format
