import duckdb
import pandas as pd

def load_append(csv_path="PCPI25M2.csv", db_path="cpi_data.db", table_name="cpi_append"):
    df_new = pd.read_csv(csv_path)
    
    conn = duckdb.connect(db_path)
    conn.execute(f"INSERT INTO {table_name} SELECT * FROM df_new")
    conn.close()

    print(f"✅ Data from '{csv_path}' appended to table '{table_name}'.")