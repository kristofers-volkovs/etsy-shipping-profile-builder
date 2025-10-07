from pydantic import BaseModel
import datetime as dt
from typing import Any


class Address(BaseModel):
    address1: str | None
    address2: str | None = None
    zip: str
    city: str | None
    country: str
    state: str | None
    name: str | None


class Package(BaseModel):
    length: int
    width: int
    height: int
    weight: float


class CustomsItem(BaseModel):
    title: str
    quantity: int
    value: float
    country_of_origin: str
    weight: float
    hs_code: str


class Shipments(BaseModel):
    package: Package
    customs_items: list[CustomsItem]


class ShippingRatesReq(BaseModel):
    sender_address: Address
    shipments: list[Shipments]
    recipient_address: Address | None
    # extras: Extras | None
    # customs: Customs | None


# ===


class DeliveryEstimate(BaseModel):
    from_date: dt.datetime
    to_date: dt.datetime


class Rates(BaseModel):
    carrier: str
    service: str
    price: float
    currency: str
    name: str
    delivery_type: str
    courier_available: str | None
    parcelshop_id: str | None
    delivery_estimate: DeliveryEstimate | None
    promo_price: float | None
    promo_date: dt.datetime | None
    is_custom_carrier_credentials: bool
    is_customs_details_required: bool
    is_paperless_document_upload_available: bool


class ShippingRatesRes(BaseModel):
    rates: list[Rates]
    errors: dict[str, Any]
