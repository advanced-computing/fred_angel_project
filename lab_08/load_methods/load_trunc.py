import duckdb
import pandas as pd

def load_trunc(csv_path="PCPI25M2.csv", db_path="cpi_data.db", table_name="cpi_trunc"):
    df_new = pd.read_csv(csv_path)
    conn = duckdb.connect(db_path)

    conn.execute(f"DELETE FROM {table_name}")

    conn.execute(f"INSERT INTO {table_name} SELECT * FROM df_new")

    conn.close()
    print(f"✅ Table '{table_name}' was truncated and reloaded from '{csv_path}'.")