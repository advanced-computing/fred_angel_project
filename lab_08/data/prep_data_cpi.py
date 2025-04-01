import pandas as pd

def generate_cpi_csvs(excel_path: str, output_dir: str = "."):
    df = pd.read_excel(excel_path)

    df_24 = df[["DATE", "PCPI24M1"]].copy()
    df_24.rename(columns={"PCPI24M1": "CPI"}, inplace=True)
    df_24.to_csv(f"{output_dir}/PCPI24M1.csv", index=False)

    df_25 = df[["DATE", "PCPI25M2"]].copy()
    df_25.rename(columns={"PCPI25M2": "CPI"}, inplace=True)
    df_25.to_csv(f"{output_dir}/PCPI25M2.csv", index=False)

    print("✅ CSV files generated.")

if __name__ == "__main__":
    generate_cpi_csvs("pcpiMvMd.xlsx")
