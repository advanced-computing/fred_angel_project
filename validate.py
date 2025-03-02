from flask import jsonify
from error_handling import handle_invalid_parameters, handle_invalid_filter_key, handle_invalid_country

def validate_limit_offset(request_args):
    """Validates 'limit' and 'offset' parameters."""
    try:
        limit = int(request_args.get("limit", 10))
        offset = int(request_args.get("offset", 0))

        if limit < 1 or offset < 0:
            return False, handle_invalid_parameters()
                
        return True, (limit, offset)  # Return valid values if they pass the check

    except ValueError:
            return False, handle_invalid_parameters()
        
# Define valid API parameters explicitly
#   Note: Could be dynamic, but since the app is simple uses list
VALID_PARAMS = {"limit", "offset", "format", "Region Code"}  # Add other accepted filter parameters

def validate_filter_keys(request_args):
    """Validates if provided filter keys match the allowed API parameters."""
    for key in request_args.keys():
        if key not in VALID_PARAMS:
            return False, handle_invalid_filter_key(key)
        
    return True, None  # Return True if all keys are valid


def validate_country(request_args, valid_countries):
    """Validates if the country name provided is in the dataset."""
    if "Country" in request_args:
        country = request_args["Country"]
        if country not in valid_countries:
            return False, handle_invalid_country(country), 400
        
    return True, None, 200  # Return True if the country is valid
