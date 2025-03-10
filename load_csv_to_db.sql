ATTACH DATABASE 'un_data.db' AS mydb;

CREATE TABLE IF NOT EXISTS mydb.users (
    username TEXT PRIMARY KEY,
    age INTEGER,
    country TEXT
);

CREATE TABLE IF NOT EXISTS mydb.un_data (
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
    column1 AS Country,
    CAST(Year AS INTEGER) AS Year,
    Series,
    CAST(REPLACE(Value, ',', '') AS FLOAT) AS Value,
    Footnotes,
    Source
FROM read_csv_auto(
    'https://raw.githubusercontent.com/advanced-computing/fred_angel_project/main/un_data.csv',
    skip=1,
    ignore_errors=true, 
    all_varchar=true
);