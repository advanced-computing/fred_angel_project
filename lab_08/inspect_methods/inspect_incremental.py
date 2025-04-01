import duckdb

def inspect_table(table_name="cpi_inc", db_path="cpi_data.db"):
    conn = duckdb.connect(db_path)
    
    count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    print(f"🔎 {table_name} has {count} rows.")
    
    print("\nSample rows:")
    sample = conn.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchdf()
    print(sample)

    conn.close()

if __name__ == "__main__":
    inspect_table()