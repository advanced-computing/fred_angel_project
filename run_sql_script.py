import duckdb

DB_PATH = "un_data.db"

def run_sql_script():
    
    try:
        
        with duckdb.connect(database=":memory:") as conn:
            with open("load_csv_to_db.sql", "r", encoding="utf-8") as f:
                conn.execute(f.read())

            un_data_count = conn.execute("SELECT COUNT(*) FROM mydb.un_data").fetchone()
            users_count = conn.execute("SELECT COUNT(*) FROM mydb.users").fetchone()
            print(f"Loaded {un_data_count[0]} records into 'un_data' table.")
            print(f"Loaded {users_count[0]} records into 'un_data' table.")
            
    except duckdb.IOException as e:
        print("Error: Database file is locked. Trying a workaround...")
        print(e)

if __name__ == "__main__":
    run_sql_script()