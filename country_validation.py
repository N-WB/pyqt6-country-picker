import typing
from typing import Any
from typing import Callable


def validate_list_of_entries(   
          maybe_list: Any
        , per_item_validator: Callable[[Any], bool]
    ) -> bool:
    '''Validates all entries in the list and only returns True if they all succeed.'''

    if not isinstance(maybe_list, list):
        return False
    
    for item in maybe_list:
        is_item_valid: bool = per_item_validator(item)
        if not is_item_valid:
            return False
        
    return True


def check_country_has_name(country_object: Any) -> bool:
    return "name" in country_object and isinstance(country_object["name"], str)


def do_full_country_list_validation(countries_list: Any) -> bool:
    '''Do all the necessary checking to ensure that a country's data is correctly arranged.'''

    # ponder - consider doing full validation of all the fields of the country versus just the field "name" that we need

    # N.B. the types implied by the countries API documentation are ambiguous
    # In the API, only 165 countries have a "borders" attribute, despite the fact that "https://www.apicountries.com/docs/api/countries"
    # implies that the borders attribute is present on all entries.
    # Thus, I undid a change where I was testing all fields.

    return validate_list_of_entries(countries_list, check_country_has_name)

