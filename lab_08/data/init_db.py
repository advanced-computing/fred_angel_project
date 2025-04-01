import duckdb
import pandas as pd

def init_cpi_database(csv_path="PCPI24M1.csv", db_path="cpi_data.db"):
    df = pd.read_csv(csv_path)

    conn = duckdb.connect(db_path)

    for table in ["cpi_append", "cpi_trunc", "cpi_inc"]:
        conn.execute(f"DROP TABLE IF EXISTS {table}")
        conn.execute(f"""
            CREATE TABLE {table} AS
            SELECT * FROM df
        """)
        print(f"Table '{table}' created and initialized.")

    conn.close()
    print(f"\n Database '{db_path}' is ready with 3 initialized tables.")

if __name__ == "__main__":
    init_cpi_database()