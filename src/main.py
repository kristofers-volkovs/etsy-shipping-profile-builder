from dotenv import load_dotenv
from os.path import isdir, isfile, join
from os import listdir
from api.api_swotzy import ApiSwotzy
from data_loader import CountryDataLoader
from schemas.rates import Address, Package, CustomsItem, ShippingRatesReq, Shipments
from utils import get_env, load_json_file

load_dotenv()


def get_dir_filepaths(*, dir_path: str) -> list[str]:
    if not isdir(dir_path):
        raise ValueError(f"{dir_path=} is not a directory")

    return [f"{dir_path}/{f}" for f in listdir(dir_path) if isfile(join(dir_path, f))]


def main():
    api_client = ApiSwotzy()

    filepath = "data/country/austria.csv"
    country_data = CountryDataLoader.load_csv(filepath=filepath)
    alpha_2 = country_data.alpha_2

    package_dict = load_json_file(filepath="data/package.json")
    package = Package(**package_dict, weight=0.2)

    customs_items_dict = load_json_file(filepath="data/customs_item.json")
    customs_items = CustomsItem(
        **customs_items_dict,
        weight=0.2,
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
    customs_items = CustomsItem(
        title="Example product",
        quantity=1,
        value=19.99,
        country_of_origin=get_env("SENDER_COUNTRY"),
        weight=0.2,
        hs_code="392690",
    )

    for country_data_row in country_data.data:
        recipient_address = Address(
            address1=country_data_row.street,
            zip=country_data_row.zip_code,
            city=country_data_row.city,
            country=alpha_2,
            state=country_data_row.state,
            name="Test Name",
        )
        request = ShippingRatesReq(
            sender_address=sender_address,
            shipments=[Shipments(package=package, customs_items=[customs_items])],
            recipient_address=recipient_address,
        )

        res = api_client.get_rates(request=request)
        print(res.rates[0])
        print("===")

    print("end")


if __name__ == "__main__":
    main()
