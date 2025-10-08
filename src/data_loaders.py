import json
from typing import Any
import csv
from schemas.country import CountryData, CountryDataRow
from utils import extract_filename, convert_country_to_alpha_2


def load_json_file(*, filepath: str) -> dict[str, Any]:
    with open(filepath, "r") as f:
        return json.load(f)


def load_country_csv(*, filepath: str, drop_header: bool = True) -> CountryData:
    filename = extract_filename(filepath=filepath)
    alpha_2 = convert_country_to_alpha_2(country_name=filename)

    country_data_rows: list[CountryDataRow] = []

    with open(filepath, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            country_data_row = CountryDataRow(
                street=f"{row[0]} {row[1]}",
                city=row[3],
                state=row[4],
                zip_code=row[5],
            )
            country_data_rows.append(country_data_row)

    if drop_header:
        start_idx = 1
    else:
        start_idx = 0

    country_data = CountryData(
        country=filename, alpha_2=alpha_2, data=country_data_rows[start_idx:]
    )

    return country_data
