from settings import Settings
from schemas.rates import Address, Package, CustomsItem
from schemas.country import CountryDataRow


def build_sender(*, settings: Settings) -> Address:
    return Address(
        address1=settings.SENDER_ADDRESS,
        zip=settings.SENDER_ZIP,
        city=settings.SENDER_CITY,
        country=settings.SENDER_COUNTRY,
        state=settings.SENDER_STATE,
        name=settings.SENDER_NAME,
    )


def build_recipient(*, country_row: CountryDataRow, alpha_2: str) -> Address:
    return Address(
        address1=country_row.street,
        zip=country_row.zip_code,
        city=country_row.city,
        country=alpha_2,
        state=country_row.state,
        name="I'm Batman",
    )


def build_package(*, settings: Settings) -> Package:
    return Package(
        height=settings.PACKAGE_HEIGHT,
        length=settings.PACKAGE_LENGTH,
        width=settings.PACKAGE_WIDTH,
        weight=settings.PACKAGE_WEIGHT,
    )


def build_customs_item(*, settings: Settings) -> CustomsItem:
    return CustomsItem(
        title=settings.CUSTOMS_ITEM_TITLE,
        country_of_origin=settings.CUSTOMS_ITEM_COUNTRY_OF_ORIGIN,
        quantity=settings.CUSTOMS_ITEM_QUANTITY,
        value=settings.CUSTOMS_ITEM_VALUE,
        weight=settings.CUSTOMS_ITEM_WEIGHT,
        hs_code=settings.CUSTOMS_ITEM_HS_CODE,
    )
