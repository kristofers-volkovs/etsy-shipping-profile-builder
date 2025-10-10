from pathlib import Path
from schemas.country import CountryData, CountryDataRow
import csv
from utils.utils import country_to_alpha_2


class CsvCountryLoader():
    def load(self, *, path: Path) -> CountryData:
        filename = path.stem
        alpha_2 = country_to_alpha_2(country_name=filename)

        rows: list[CountryDataRow] = []
        with path.open() as f:
            reader = csv.DictReader(f)
            required = ["Street", "HouseNumber", "Region", "Province", "PostalCode"]

            missing_cols = set(required).difference(reader.fieldnames or [])
            if missing_cols:
                raise ValueError(f"Missing columns {missing_cols}, {path=}")

            for row in reader:
                country_data_row = CountryDataRow(
                    street=f"{row['Street']} {row['HouseNumber']}",
                    city=row["Region"],
                    state=row["Province"],
                    zip_code=row["PostalCode"],
                )
                rows.append(country_data_row)

        country_data = CountryData(country=filename, alpha_2=alpha_2, data=rows)
        return country_data
