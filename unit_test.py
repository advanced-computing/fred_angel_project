import pytest
from flask import Flask
from main import app
from helper import load_data, filter_and_paginate
import pandas as pd

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

### Test that checks that the home path produces the right answer.
def test_home(client):
    """Test if the home route returns the correct response."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Flask API is running" in response.data

### Test that checks the data loads to be accurate and nonempty.
def test_load_data():
    """Test if the data loads correctly."""
    df = load_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty, "DataFrame should not be empty"
    
### Test that filtering data by a specific column name to check filters. American = USA
def test_filter_by_column():
    """Test filtering data by a specific column."""
    df = pd.DataFrame({"Country": ["American", "Canada", "Mexico"], "Population": [300, 37, 128]})
    params = {"Country": "USA"}
    filtered_df, _ = filter_and_paginate(df, params)
    assert len(filtered_df) == 1, "Should return only rows where Country is 'USA'"

### Test that verifies pagination works.
def test_pagination():
    """Test pagination functionality."""
    df = pd.DataFrame({"ID": range(10)})
    params = {"limit": 5, "offset": 2}
    paginated_df, _ = filter_and_paginate(df, params)
    assert len(paginated_df) == 5, "Pagination should return 5 rows"
    assert paginated_df.iloc[0]["ID"] == 2, "First item should start at offset 2"