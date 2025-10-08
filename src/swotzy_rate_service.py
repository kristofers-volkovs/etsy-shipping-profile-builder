from api.api_swotzy import ApiSwotzyBase
from utils import get_dir_filepaths
from data_loaders import load_country_csv, load_json_file
from schemas.rates import (
    Address,
    Package,
    CustomsItem,
    ShippingRatesReq,
    Shipments,
    Rates,
)
from schemas.country import CountryData
from utils import get_env


class SwotzyRateService:
    def __init__(self, *, api_client: ApiSwotzyBase) -> None:
        self._api_client = api_client

    def _get_country_rates(
        self,
        *,
        package: Package,
        customs_item: CustomsItem,
        country_data: CountryData,
        sender_address: Address,
    ) -> list[Rates]:
        country_rates: list[Rates] = []

        for country_data_row in country_data.data:
            recipient_address = Address(
                address1=country_data_row.street,
                zip=country_data_row.zip_code,
                city=country_data_row.city,
                country=country_data.alpha_2,
                state=country_data_row.state,
                name="Batman",
            )
            req = ShippingRatesReq(
                sender_address=sender_address,
                shipments=[Shipments(package=package, customs_items=[customs_item])],
                recipient_address=recipient_address,
            )
            res = self._api_client.get_rates(req=req)

            if not res.errors:
                country_rates.extend(res.rates)
            else:
                raise Exception(f"Swotzy API call failed, error: {res.errors}")

        return country_rates

    def compute_all_destination_country_rates(
        self,
        *,
        country_dir_path: str,
        package_filepath: str,
        customs_item_filepath: str,
    ) -> None:
        country_filepaths = get_dir_filepaths(dir_path=country_dir_path)
        for country_filepath in country_filepaths:
            self.compute_destination_country_rates(
                country_filepath=country_filepath,
                package_filepath=package_filepath,
                customs_item_filepath=customs_item_filepath,
            )

    def compute_destination_country_rates(
        self,
        *,
        country_filepath: str,
        package_filepath: str,
        customs_item_filepath: str,
    ) -> None:
        package_dict = load_json_file(filepath=package_filepath)
        customs_item_dict = load_json_file(filepath=customs_item_filepath)

        weight = 0.2
        package = Package(**package_dict, weight=weight)
        customs_item = CustomsItem(
            **customs_item_dict,
            weight=weight,
            country_of_origin=get_env("SENDER_COUNTRY"),
        )

        sender_address = Address(
            address1=get_env("SENDER_ADDRESS"),
            zip=get_env("SENDER_ZIP"),
            city=get_env("SENDER_CITY"),
            country=get_env("SENDER_COUNTRY"),
            state=get_env("SENDER_STATE"),
            name=get_env("SENDER_NAME"),
        )

        country_data = load_country_csv(filepath=country_filepath)

        country_rates = self._get_country_rates(
            package=package,
            customs_item=customs_item,
            country_data=country_data,
            sender_address=sender_address,
        )
        print(len(country_rates))
