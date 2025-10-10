import httpx
from schemas.rates import ShippingRatesReq, ShippingRatesRes


class SwotzyClient:
    def __init__(
        self, *, base_url: str, auth: httpx.Auth, client: httpx.Client | None = None
    ) -> None:
        self.__base_url = base_url
        self.__client = client or httpx.Client(auth=auth)

    def get_rates(self, *, req: ShippingRatesReq) -> ShippingRatesRes:
        url = self.__base_url + "/rates"
        data = req.model_dump(mode="json")

        res = self.__client.post(url, json=data, headers={"Accept": "application/json"})
        if res.status_code != 200:
            raise ValueError(f"Swotzy /rates failed, {res.status_code}", res.content)
        return ShippingRatesRes(**res.json())
