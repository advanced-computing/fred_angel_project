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

### Test that checks that the home path produces the right answer.:
def test_home(client):
    """Test if the home route returns the correct response."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Flask API is running" in response.data

### Test that checks the data loads to be accurate and nonempty.:
def test_load_data():
    """Test if the data loads correctly."""
    df = load_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty, "DataFrame should not be empty"