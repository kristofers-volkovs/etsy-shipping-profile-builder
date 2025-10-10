from pydantic_settings import BaseSettings
from pydantic import computed_field


class Settings(BaseSettings):
    PUBLIC_KEY: str
    PRIVATE_KEY: str

    SENDER_ADDRESS: str
    SENDER_ZIP: str
    SENDER_CITY: str
    SENDER_COUNTRY: str
    SENDER_STATE: str
    SENDER_NAME: str

    PACKAGE_LENGTH: int = 16
    PACKAGE_WIDTH: int = 16
    PACKAGE_HEIGHT: int = 7
    PACKAGE_WEIGHT: float = 0.2

    CUSTOMS_ITEM_TITLE: str = "Example product"
    CUSTOMS_ITEM_QUANTITY: int = 1
    CUSTOMS_ITEM_VALUE: float = 19.99
    CUSTOMS_ITEM_HS_CODE: str = "392690"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def CUSTOMS_ITEM_WEIGHT(self) -> float:
        return self.PACKAGE_WEIGHT

    @computed_field  # type: ignore[prop-decorator]
    @property
    def CUSTOMS_ITEM_COUNTRY_OF_ORIGIN(self) -> str:
        return self.SENDER_COUNTRY


def get_settings() -> Settings:
    return Settings()  # type: ignore
