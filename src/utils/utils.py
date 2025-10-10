import pycountry
import datetime as dt
from clock import Clock


def country_to_alpha_2(*, country_name: str) -> str:
    alpha_2_dict = {
        "turkey": "TR",
        "united-kingdom": "GB",
        "united-states-of-america": "US",
    }

    if country_name in alpha_2_dict.keys():
        return alpha_2_dict[country_name]

    try:
        return pycountry.countries.lookup(value=country_name).alpha_2
    except LookupError as e:
        raise ValueError(f"No alpha-2 for '{country_name}'") from e


def calc_today_to_date_delta_days(
    *,
    to_date: dt.datetime,
    clock: Clock,
) -> int:
    today = clock.today()
    return (to_date.date() - today).days
