import duckdb

DB_PATH = "un_data.db"

def run_sql_script():
    with duckdb.connect(DB_PATH) as conn:
        with open("load_csv_to_db.sql", "r", encoding="utf-8") as f:
            conn.execute(f.read())

        result = conn.execute("SELECT COUNT(*) FROM mydb.un_data").fetchone()
        print(f"Loaded {result[0]} records into 'un_data' table.")

if __name__ == "__main__":
    run_sql_script()