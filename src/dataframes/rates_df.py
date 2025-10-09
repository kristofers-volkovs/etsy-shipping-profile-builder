from schemas.rates import Rates
from enum import Enum
from utils import calc_today_to_date_delta_days
import pandas as pd
from os.path import isdir
import os
import numpy as np


class RatesDfCols(Enum):
    carrier = "carrier"
    service = "service"
    price = "price"
    delivery_estimate_min = "delivery_estimate_min"
    delivery_estimate_max = "delivery_estimate_max"
    type = "type"


class DeliveryType(Enum):
    standard = "standard"
    express = "express"


class RatesDataFrame:
    def __init__(
        self,
        *,
        country_name: str,
        country_rates: list[Rates],
        remove_untracked: bool = True,
    ) -> None:
        rates_dict: dict[str, list[str | int | float]] = {
            RatesDfCols.carrier.value: [],
            RatesDfCols.service.value: [],
            RatesDfCols.price.value: [],
            RatesDfCols.delivery_estimate_min.value: [],
            RatesDfCols.delivery_estimate_max.value: [],
        }
        untracked_carrier = "LATVIJAS_PASTS"
        untracked_service = "SIMPLE"

        for rates in country_rates:
            if rates.delivery_estimate is None:
                print(
                    f"Missing delivery estimate for {country_name} - {rates.carrier} {rates.service}, skipping..."
                )
                continue

            if (
                remove_untracked
                and rates.carrier == untracked_carrier
                and rates.service == untracked_service
            ):
                continue

            rates_dict[RatesDfCols.carrier.value].append(rates.carrier)
            rates_dict[RatesDfCols.service.value].append(rates.service)
            rates_dict[RatesDfCols.price.value].append(rates.price)

            delivery_estimate_min = calc_today_to_date_delta_days(
                to_date=rates.delivery_estimate.from_date
            )
            delivery_estimate_max = calc_today_to_date_delta_days(
                to_date=rates.delivery_estimate.to_date
            )
            rates_dict[RatesDfCols.delivery_estimate_min.value].append(
                delivery_estimate_min
            )
            rates_dict[RatesDfCols.delivery_estimate_max.value].append(
                delivery_estimate_max
            )

        self.__df = pd.DataFrame(rates_dict)
        self.__country_name = country_name
        self.__output_dir = "data/country_rates"

    def save_country_rates(self) -> None:
        filepath = f"{self.__output_dir}/{self.__country_name}-rates.csv"
        if os.path.exists(filepath):
            print("File {filepath} already exists, skipping...")

        price_col = RatesDfCols.price.value
        delivery_estimate_min_col = RatesDfCols.delivery_estimate_min.value
        delivery_estimate_max_col = RatesDfCols.delivery_estimate_max.value

        # Aggregate and compute mean for the same carrier and service rows
        df_avg = self.__df.groupby(
            [RatesDfCols.carrier.value, RatesDfCols.service.value], as_index=False
        ).agg(
            {
                price_col: "mean",
                delivery_estimate_min_col: lambda x: np.ceil(x.mean()),
                delivery_estimate_max_col: lambda x: np.ceil(x.mean()),
            }
        )

        min_price_idx = df_avg[price_col].idxmin()

        # Filters out high prices and long delivery times
        max_delivery_price = 35
        max_delivery_estimate_min = df_avg.loc[min_price_idx][delivery_estimate_min_col]
        max_delivery_estimate_max = df_avg.loc[min_price_idx][delivery_estimate_max_col]
        df_filtered = df_avg[
            (df_avg[price_col] <= max_delivery_price)
            & (df_avg[delivery_estimate_min_col] < max_delivery_estimate_min)
            & (df_avg[delivery_estimate_max_col] < max_delivery_estimate_max)
        ]

        # Selects the shortest delivery time with the lowest time
        if len(df_filtered) > 0:
            min_delivery_time_idx = df_filtered.sort_values(
                by=[delivery_estimate_min_col, price_col]
            ).index[0]
        else:
            min_delivery_time_idx = min_price_idx

        df_rates = df_avg.loc[[min_price_idx, min_delivery_time_idx]]
        # Note: the order of types needs to correspond with the indexes, otherwise could cause a bug
        df_rates[RatesDfCols.type.value] = [
            DeliveryType.standard.value,
            DeliveryType.express.value,
        ]

        # Checks if dir exists - if not then creates it
        if not isdir(self.__output_dir):
            os.makedirs(self.__output_dir)

        df_rates.to_csv(filepath, index=False)

    def print_df(self):
        print(self.__df.to_string())
