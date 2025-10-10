from schemas.rates import Rate
import pandas as pd
from utils.utils import calc_today_to_date_delta_days
from typing import Callable
import numpy as np
from clock import Clock


RATES_DF_COLS = {
    "carrier": "carrier",
    "service": "service",
    "price": "price",
    "est_min": "delivery_estimate_min",
    "est_max": "delivery_estimate_max",
    "delivery_type": "delivery_type",
}

DELIVERY_TYPE = {
    "standard": "standard",
    "express": "express",
}


def remove_untracked_option(rate: Rate) -> bool:
    return rate.carrier == "LATVIJAS_PASTS" and rate.service == "SIMPLE"


def rates_to_dataframe(
    *,
    country_name: str,
    country_rates: list[Rate],
    remove_predicate: Callable[[Rate], bool] = lambda _: False,
    clock: Clock,
) -> pd.DataFrame:
    rates_list: list[dict[str, str | int | float]] = []

    for rate in country_rates:
        if rate.delivery_estimate is None:
            print(
                "Missing delivery estimate for %s - %s %s, skipping",
                country_name,
                rate.carrier,
                rate.service,
            )
            continue
        if remove_predicate(rate):
            continue  # This rate is skipped

        rates_list.append(
            {
                RATES_DF_COLS["carrier"]: rate.carrier,
                RATES_DF_COLS["service"]: rate.service,
                RATES_DF_COLS["price"]: rate.price,
                RATES_DF_COLS["est_min"]: calc_today_to_date_delta_days(
                    to_date=rate.delivery_estimate.from_date, clock=clock
                ),
                RATES_DF_COLS["est_max"]: calc_today_to_date_delta_days(
                    to_date=rate.delivery_estimate.to_date, clock=clock
                ),
            }
        )

    return pd.DataFrame(rates_list)


def average_rates(*, df: pd.DataFrame) -> pd.DataFrame:
    df_avg = df.groupby(
        [RATES_DF_COLS["carrier"], RATES_DF_COLS["service"]], as_index=False
    ).agg(
        {
            RATES_DF_COLS["price"]: "mean",
            RATES_DF_COLS["est_min"]: lambda x: int(np.ceil(np.mean(x))),
            RATES_DF_COLS["est_max"]: lambda x: int(np.ceil(np.mean(x))),
        }
    )
    return df_avg


def filter_rates(*, df: pd.DataFrame, max_delivery_price: float) -> pd.DataFrame:
    min_price_idx = df[RATES_DF_COLS["price"]].idxmin()
    est_min = df.loc[min_price_idx][RATES_DF_COLS["est_min"]]
    est_max = df.loc[min_price_idx][RATES_DF_COLS["est_max"]]

    df_filtered = df[
        (df[RATES_DF_COLS["price"]] <= max_delivery_price)
        & (df[RATES_DF_COLS["est_min"]] <= est_min)
        & (df[RATES_DF_COLS["est_max"]] < est_max)
    ]
    return df_filtered


def select_rates(*, df_avg: pd.DataFrame, df_filtered: pd.DataFrame) -> pd.DataFrame:
    min_price_idx = df_avg[RATES_DF_COLS["price"]].idxmin()

    if not df_filtered.empty:
        min_delivery_time_idx = df_filtered.sort_values(
            by=[RATES_DF_COLS["est_min"], RATES_DF_COLS["price"]]
        ).index[0]
    else:
        min_delivery_time_idx = min_price_idx

    df_rates = df_avg.loc[[min_price_idx, min_delivery_time_idx]]
    # Note: the order of types needs to correspond with the indexes, otherwise could cause a bug
    df_rates[RATES_DF_COLS["delivery_type"]] = [
        DELIVERY_TYPE["standard"],
        DELIVERY_TYPE["express"],
    ]
    return df_rates
