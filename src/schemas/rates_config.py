from pydantic import BaseModel


class RatesConfig(BaseModel):
    rates_sample_limit: int = 3
    override_file: bool = False
    max_delivery_price: float = 35
