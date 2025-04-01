import duckdb
import pandas as pd

def load_incremental(csv_path="PCPI25M2.csv", db_path="cpi_data.db", table_name="cpi_inc"):
    df_new = pd.read_csv(csv_path)
    conn = duckdb.connect(db_path)

    conn.execute("CREATE OR REPLACE TEMP TABLE temp_new AS SELECT * FROM df_new")

    conn.execute(f"""
        DELETE FROM {table_name}
        WHERE DATE IN (SELECT DATE FROM temp_new)
    """)

    conn.execute(f"INSERT INTO {table_name} SELECT * FROM temp_new")

    conn.close()
    print(f"✅ Table '{table_name}' was updated incrementally from '{csv_path}'.")
