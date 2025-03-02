import pytest
import pandas as pd
from helper import load_data

def test_missing_values():
    df = load_data()
    assert df["Year"].notnull().all(), "Missing values found in Year column"
    assert df["Value"].notnull().all(), "Missing values found in Value column"
    assert df["Country"].notnull().all(), "Missing values found in Country column"

def test_data_types():
    df = load_data()
    assert df["Year"].dtype in ["int64", "float64"], "Year column is not int64 or float64"
    df["Value"] = pd.to_numeric(df["Value"].astype(str).str.replace(",", ""), errors='coerce')
    assert df["Value"].dtype == "float64", "Value column is not float64"

def test_value_distribution():
    df = load_data()
    assert df["Year"].between(1900, 2025).all(), "Some Year values are out of range"

def test_standard_deviation():
    df = load_data()
    df["Value"] = pd.to_numeric(df["Value"].astype(str).str.replace(",", ""), errors='coerce')
    std_dev = df["Value"].std()
    assert 0 < std_dev < 10000, "Value column has an abnormal standard deviation"

def test_value_range():
    df = load_data()
    df["Value"] = pd.to_numeric(df["Value"].astype(str).str.replace(",", ""), errors='coerce')
    lower_bound, upper_bound = df["Value"].quantile([0.05, 0.95])
    valid_values = df["Value"].between(lower_bound, upper_bound).sum()
    assert valid_values / len(df) > 0.9, "Less than 90% of values are within the expected range"

if __name__ == "__main__":
    pytest.main()