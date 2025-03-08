from error_handling import (
    handle_invalid_parameters,
    handle_invalid_filter_key,
    handle_invalid_country,
    handle_bad_request
)

def validate_all_filters(params, valid_countries):
    
    validated_filters = {}

    try:
        limit = int(params.get("limit", 10))
        offset = int(params.get("offset", 0))

        if limit <= 0 or offset < 0:
            return handle_invalid_parameters()
        
        validated_filters["limit"] = limit
        validated_filters["offset"] = offset

    except ValueError:
        return handle_invalid_parameters()

    if "Year" in params:
        try:
            validated_filters["Year"] = int(params["Year"])
        except ValueError:
            return handle_bad_request("Invalid year format. Must be a number.")

    country = params.get("Country")
    if country and country not in valid_countries:
        return handle_invalid_country(country)
    validated_filters["Country"] = country

    valid_keys = {"Region_Code", "Country", "Year", "Series", "Value", "Footnotes", "Source"}

    for key in params.keys():
        if key not in valid_keys and key not in ["limit", "offset", "format"]:  
            return handle_invalid_filter_key(key)

    return validated_filters
