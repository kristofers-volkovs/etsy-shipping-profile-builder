import os
import pycountry
import json
from typing import Any


def get_env(key: str) -> str:
    env_variable = os.getenv(key)
    if env_variable is None or env_variable == "changethis":
        raise Exception(f"Variable '{key}' not set in .env file")

    return env_variable


def convert_country_to_alpha_2(*, country_name: str) -> str:
    try:
        country = pycountry.countries.get(name=country_name)
        return country.alpha_2
    except AttributeError:
        raise Exception(f"Alpha 2 value missing for {country_name}")


def extract_filename(*, filepath: str) -> str:
    return filepath.split("/")[-1].split(".")[0]


def load_json_file(*, filepath: str) -> dict[str, Any]:
    with open(filepath, "r") as f:
        return json.load(f)
