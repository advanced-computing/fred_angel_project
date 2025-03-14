import duckdb
from error_handling import handle_server_error

DB_PATH = "un_data.db"
COLUMN_ORDER = ["Region_Code", "Country", "Year", "Series", "Value", "Footnotes", "Source"]

def initialize_database():
    conn = duckdb.connect(DB_PATH)
    conn.close()

def get_valid_countries():
    try:
        conn = duckdb.connect(DB_PATH)
        countries = conn.execute("SELECT DISTINCT Country FROM un_data").fetchdf()["Country"].tolist()
        conn.close()
        return set(countries)
    except Exception as e:
        return handle_server_error(e)

def filter_and_paginate(filters):
    try:
        query = f"SELECT {', '.join(COLUMN_ORDER)} FROM un_data WHERE 1=1"
        conditions = []

        if "Year" in filters:
            conditions.append(f"AND Year = {filters['Year']}")
        if "Country" in filters:
            conditions.append(f"AND Country = '{filters['Country']}'")
        if "Series" in filters:
            conditions.append(f"AND Series LIKE '%{filters['Series']}%'")

        filter_query = " ".join(conditions)
        final_query = f"{query} {filter_query} ORDER BY {', '.join(COLUMN_ORDER)} LIMIT {filters.get('limit', 10)} OFFSET {filters.get('offset', 0)}"

        conn = duckdb.connect(DB_PATH)
        df = conn.execute(final_query).fetchdf()
        conn.close()

        if not df.empty:
            df["Value"] = df["Value"].apply(lambda x: round(x, 1) if isinstance(x, (int, float)) else x)

        return df

    except Exception as e:
        return handle_server_error(e)
    
def add_user(username, age, country):
    try:
        conn = duckdb.connect(DB_PATH)
        conn.execute(
            "INSERT INTO users (username, age, country) VALUES (?, ?, ?)",
            (username, age, country)
        )
        conn.close()
        return {"message": "User added successfully"}
    except Exception as e:
        return handle_server_error(e)