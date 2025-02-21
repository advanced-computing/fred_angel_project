import pandas as pd
from helper_functions import continent_filter


#Funny enough, United States is listed as American
def test_continent_filter():
    countries = pd.Series(
        [
            "Africa",
            "Angola",
            "United States"
            None,
        ]
    )

    result = continent_filter(countries)
    expected = pd.Series(
        [
            None,
            "Angola",
            "United States"
            None,
        ]
    )
    
    assert result.equals(expected)
