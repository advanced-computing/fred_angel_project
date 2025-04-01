
# Lab 08 — CPI Data Loading with DuckDB

**Fred Lee and Angel Ragas**

## Documentation-Driven Development

This project follows a documentation-first approach. All methods were specified, tested, and documented before or alongside development. Testing scripts and expected outcomes were explicitly defined to guide implementation and ensure correctness. Additionally, we have organized the files in folders, depending on their type and importance.

## Objective

Our task uses the following CPI data from the Federal Reserve Bank of Philadelphia:

- **PCPI24M1.csv**: January 2024
- **PCPI25M2.csv**: February 2025 (including historical revisions and new rows)

---

## Project Structure

```
lab_08/
├── data/
│   ├── PCPI24M1.csv
│   ├── PCPI25M2.csv
│   ├── pcpiMvMd.xlsx
│   ├── prep_data_cpi.py
│   └── cpi_data.db
│
├── load_methods/
│   ├── load_append.py
│   ├── load_trunc.py
│   └── load_incremental.py
│
├── test_methods/
│   ├── test_append.py
│   ├── test_trunc.py
│   └── test_incremental.py
│
├── inspect_methods/
│   ├── inspect_append.py
│   ├── inspect_trunc.py
│   └── inspect_incremental.py
│
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate the two CSVs from Excel

```bash
python data/prep_data_cpi.py
```

### 3. Initialize the database with PCPI24M1.csv

```bash
python data/init_db.py
```

This will create a `cpi_data.db` file with 3 identical tables:
- `cpi_append`
- `cpi_trunc`
- `cpi_inc`

Each is initialized with 937 rows.

---

## How to Run Each Method

### 1. Append Method

- Run:
  ```bash
  python test_methods/test_append.py
  ```

- Inspect:
  ```bash
  python inspect_methods/inspect_append.py
  ```

- Result:
  - Table now has **1874 rows**
  - Full second file was appended to the original
  - **Duplicates are present** for overlapping dates

---

### 2. Truncate Method

- Run:
  ```bash
  python test_methods/test_trunc.py
  ```

- Inspect:
  ```bash
  python inspect_methods/inspect_trunc.py
  ```

- Result:
  - Table has **937 rows**
  - Fully replaced with February 2025 snapshot
  - **No duplicates**, but **January 2024 snapshot is erased**

---

### 3. Incremental Method

- Run:
  ```bash
  python test_methods/test_incremental.py
  ```

- Inspect:
  ```bash
  python inspect_methods/inspect_incremental.py
  ```

- Result:
  - Table has **937 rows**
  - Matches `PCPI25M2.csv`
  - **Duplicates removed**
  - Replaces old dates, **keeps new ones (optimal for production use)**

---

## Summary of Expected Results

| Table Name     | Expected Rows    | Description                                                                      |
|----------------|------------------|----------------------------------------------------------------------------------|
| `cpi_append`   | 1874             | Includes all rows from both CSVs with expected duplicates                        |
| `cpi_trunc`    | 937              | Fully replaced with latest snapshot (Feb 2025) and no historical data retained   |
| `cpi_inc`      | 937              | Clean merge (updated rows replaced, new ones added, no duplicates)               |

---

## Method Comparison (Table)

| Method          | Rows  | Duplicates | Keeps Precedent Historic Files           |
|-----------------|-------|------------|------------------------------------------|
| **Append**      | 1874  | Yes        | Yes (but we considered it as messy)      |
| **Truncate**    | 937   | No         | No                                       | 
| **Incremental** | 937   | No         | Yes (latest only)                        |

---

## Comparison (Group Discussion)

- **Append:** Applying the add technique to the cpi_append table produced a last row count of 1874, precisely double the original 937 rows from PCPI24M1.csv. This verified that every row from the February 2025 snapshot (PCPI25M2.csv) was simply added below the prior data, regardless of whether it overlapped in dates. Although this method is quite simple to apply and needs no logic for verifying current records, it creates duplicate entries for dates already existent, which could significantly degrade data quality and distort studies if not managed downstream. Many rows were duplicated for the same months in our situation, which clearly shows that this approach is unsuitable given anticipated historical changes. Though it's inefficient and unreliable for organised analytics or longitudinal comparison, append could still be beneficial in raw logging situations or when you need to keep every ingested version of a dataset for audit reasons.

- **Truncate:** Using the truncation approach, data from PCPI25M2.csv was loaded into the cpi_trunc table after it had been totally cleaned. The resulting row count, as anticipated, reverted to 937 rows, reflecting the new file precisely. This approach ensures the database always shows the most recent snapshot available by guaranteeing no duplicate or contamination from previous data loading. This, too, has a price: any prior values that are no longer in the most recent file are lost completely, including maybe pertinent history data. This approach would become difficult, for example, if we wished to contrast January 2024 values before and after modification unless we stored the previous dataset somewhere else. Simply put, when only the most recent version of the dataset matters—for dashboards or reports that get regenerated from scratch every cycle—truncate-and-replace is a neat and quick solution.

- **Incremental:** The incremental loading technique used to the cpi_inc table produced the same number of rows as the truncate method—937 rows—but with a more subtle approach. It merely deleted entries whose dates matched those in PCPI25M2.csv, then added the revised values instead of erasing all prior data. This method let us save unique rows that didn't require change and update those that did, therefore producing a neat and efficient table without duplicates. The result showed that changes were being managed carefully without needlessly erasing the table, matching the structure of the most recent file. In production systems, particularly those managing time-series or financial data, this approach is significantly better: it's strong, prevents duplication, and reduces the possibility of unintentional data loss. When considering performance and dependability, it is the most true portrayal of how real-world data pipeline should run.

- **Overall Comparison:** The outcomes from the three approaches highlight a vital lesson in data engineering: how you load data is as important as the data itself. Though straightforward, the add technique caused uneven outcomes and enlarged tables from uncontrolled duplication. Though it sacrificed continuity by overwriting important information from prior pictures, the truncate-and-reload method produced clean outcomes. By preserving integrity, eliminating redundancy, and remaining true to the real-world situation of managing changing datasets like CPI time series, the incremental approach produced the most graceful and realistic result in contrast. Apart from technological variations, this lab emphasised the need of careful design in data loading methods.

---