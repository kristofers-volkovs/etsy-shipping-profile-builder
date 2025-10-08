from dotenv import load_dotenv
from api.api_swotzy import ApiSwotzy
from swotzy_rate_service import SwotzyRateService

load_dotenv()


def main():
    swotzy_rate_service = SwotzyRateService(api_client=ApiSwotzy())

    # swotzy_rate_service.compute_all_destination_country_rates(
    #     country_dir_path="data/country",
    #     package_filepath="data/package.json",
    #     customs_item_filepath="data/customs_item.json",
    # )

    swotzy_rate_service.compute_destination_country_rates(
        country_filepath="data/country/austria.csv",
        package_filepath="data/package.json",
        customs_item_filepath="data/customs_item.json",
    )

    print("end")


if __name__ == "__main__":
    main()
