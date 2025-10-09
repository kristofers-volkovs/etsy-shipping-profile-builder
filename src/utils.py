import os
import pycountry
from os.path import isdir, isfile, join
from os import listdir
from datetime import date
import datetime as dt


def get_env(key: str) -> str:
    env_variable = os.getenv(key)
    if env_variable is None or env_variable == "changethis":
        raise Exception(f"Variable '{key}' not set in .env file")

    return env_variable


def convert_country_to_alpha_2(*, country_name: str) -> str:
    if country_name == "turkey":
        return "TR"
    elif country_name == "united-kingdom":
        return "GB"
    elif country_name == "united-states-of-america":
        return "US"

    try:
        country = pycountry.countries.get(name=country_name)
        if country is None:
            raise Exception(f"Missing alpha2 value for: {country_name}")

        return country.alpha_2
    except AttributeError as e:
        raise Exception(f"Alpha 2 value missing for {country_name}, error: {e}")


def extract_filename(*, filepath: str) -> str:
    return filepath.split("/")[-1].split(".")[0]


def get_dir_filepaths(*, dir_path: str) -> list[str]:
    if not isdir(dir_path):
        raise ValueError(f"{dir_path=} is not a directory")

    return [f"{dir_path}/{f}" for f in listdir(dir_path) if isfile(join(dir_path, f))]


def calc_today_to_date_delta_days(*, to_date: dt.datetime) -> int:
    today = date.today()
    return (to_date.date() - today).days
