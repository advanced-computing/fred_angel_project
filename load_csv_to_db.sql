ATTACH DATABASE 'un_data.db' AS mydb;

DROP TABLE IF EXISTS mydb.un_data;

CREATE TABLE mydb.un_data (
    Region_Code INTEGER,
    Country VARCHAR,
    Year INTEGER,
    Series VARCHAR,
    Value FLOAT,
    Footnotes VARCHAR,
    Source VARCHAR
);

INSERT INTO mydb.un_data 
SELECT 
    CAST("Region/Country/Area" AS INTEGER) AS Region_Code,
    "Unnamed: 1" AS Country,
    CAST(column2 AS INTEGER) AS Year,
    column3 AS Series,
    CAST(REPLACE(column4, ',', '') AS FLOAT) AS Value,
    column5 AS Footnotes,
    column6 AS Source
FROM read_csv_auto(
    'https://raw.githubusercontent.com/advanced-computing/fred_angel_project/main/un_data.csv',
    ignore_errors=true, 
    all_varchar=true
);