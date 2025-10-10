from pydantic import BaseModel


class CountryDataRow(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str


class CountryData(BaseModel):
    country: str
    alpha_2: str
    data: list[CountryDataRow]

    def sample_rows(self, *, limit: int = 1) -> list[CountryDataRow]:
        return self.data[:limit]
