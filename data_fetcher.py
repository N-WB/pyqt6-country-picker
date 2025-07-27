import requests
import typing
from typing import Any
import country_validation


def try_fetch_countries(url: str) -> list[str] | None:
    allowed_attempts = 5

    for i in range(allowed_attempts):
        response = requests.get(url)

        try:
            jsonAsPythonObject = response.json()

            is_valid = country_validation.do_full_country_list_validation(jsonAsPythonObject)            
            if is_valid:

                def extract_name(country): return country["name"]
                country_names = [extract_name(c) for c in jsonAsPythonObject]

                return country_names
            
            else:
                print("Error: received json does not conform to the expected countries format. Retrying...")

        except requests.exceptions.JSONDecodeError as error:
            print(error)
            print("Retrying...")

    return None


        
        