from typing import Protocol
from schemas.rates import ShippingRatesReq, ShippingRatesRes


class ShippingRatesClient(Protocol):
    def get_rates(self, *, req: ShippingRatesReq) -> ShippingRatesRes: ...
