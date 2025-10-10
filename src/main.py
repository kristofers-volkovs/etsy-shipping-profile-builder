from dotenv import load_dotenv
from api.swotzy_client import SwotzyClient
from settings import get_settings
import httpx
from swotzy_rate_service import SwotzyRateService
from pathlib import Path
from data_loaders.csv_country_loader import CsvCountryLoader
from utils.builder import build_customs_item, build_package, build_sender
from clock import SystemClock
from schemas.rates_config import RatesConfig
from utils.file_writer import PdCsvWriter
from utils.filename_composer import RatesFilenameComposer


def main():
    load_dotenv()
    settings = get_settings()

    client = SwotzyClient(
        base_url="https://api.swotzy.com/public",
        auth=httpx.BasicAuth(
            username=settings.PUBLIC_KEY, password=settings.PRIVATE_KEY
        ),
    )

    swotzy_rate_service = SwotzyRateService(
        client=client,
        config=RatesConfig(),
        country_data_loader=CsvCountryLoader(),
        file_writer=PdCsvWriter(dir_path=Path("data/country_rates")),
        filename_composer=RatesFilenameComposer(),
        clock=SystemClock(),
    )

    package = build_package(settings=settings)
    customs_item = build_customs_item(settings=settings)
    sender = build_sender(settings=settings)

    # swotzy_rate_service.compute_all_rates(
    #     dir_iterator=DirFileIterator(dir_path=Path("data/country")),
    #     customs_item=customs_item,
    #     package=package,
    #     sender=sender,
    # )

    swotzy_rate_service.compute_one_rate(
        country_filepath=Path("data/country/austria.csv"),
        customs_item=customs_item,
        package=package,
        sender=sender,
    )

    print("=== end ===")


if __name__ == "__main__":
    main()
