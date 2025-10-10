from api.protocols import ShippingRatesClient
from utils.dir_iterator import DirIterator
from schemas.country import CountryData
from schemas.rates import (
    Rate,
    ShippingRatesReq,
    Address,
    Package,
    CustomsItem,
    Shipments,
)
from utils.builder import build_recipient
from data_loaders.protocols import DataLoader
from pathlib import Path
from rates_df import (
    rates_to_dataframe,
    average_rates,
    filter_rates,
    select_rates,
    remove_untracked_option,
)
import pandas as pd
from utils.file_writer import FileWriter
from schemas.rates_config import RatesConfig
from utils.filename_composer import FilenameComposer
from clock import Clock
from tqdm import tqdm


def compose_filename(*, name: str, suffix: str, extension: str) -> str:
    return name + suffix + extension


class SwotzyRateService:
    def __init__(
        self,
        client: ShippingRatesClient,
        config: RatesConfig,
        country_data_loader: DataLoader[CountryData],
        file_writer: FileWriter[pd.DataFrame],
        filename_composer: FilenameComposer,
        clock: Clock,
    ) -> None:
        self.__client = client
        self.__config = config
        self.__country_data_loader = country_data_loader
        self.__file_writer = file_writer
        self.__filename_composer = filename_composer
        self.__clock = clock

    def compute_all_rates(
        self,
        *,
        dir_iterator: DirIterator,
        sender: Address,
        package: Package,
        customs_item: CustomsItem,
    ) -> None:
        for path in tqdm(dir_iterator.iter_dir(), desc="Computing country rates"):
            self.compute_one_rate(
                country_filepath=path,
                sender=sender,
                package=package,
                customs_item=customs_item,
            )

    def compute_one_rate(
        self,
        *,
        country_filepath: Path,
        sender: Address,
        package: Package,
        customs_item: CustomsItem,
    ) -> None:
        country_data = self.__country_data_loader.load(path=country_filepath)

        rates_filename = self.__filename_composer.compose_filename(
            name=country_filepath.stem, extension=self.__file_writer.file_extension()
        )
        if self.__config.override_file and self.__file_writer.file_exists(
            filename=rates_filename
        ):
            print(f"File {rates_filename} already exists, skipping...")
            return

        country_rates: list[Rate] = []
        for row in country_data.sample_rows(limit=self.__config.rates_sample_limit):
            recipient = build_recipient(country_row=row, alpha_2=country_data.alpha_2)

            req = ShippingRatesReq(
                sender_address=sender,
                shipments=[Shipments(package=package, customs_items=[customs_item])],
                recipient_address=recipient,
            )
            res = self.__client.get_rates(req=req)

            if len(res.rates) == 0:
                raise RuntimeError(
                    f"Empty rates for {country_data.country}, error: {res.errors}"
                )
            country_rates.extend(res.rates)

        df = rates_to_dataframe(
            country_name=country_data.country,
            country_rates=country_rates,
            remove_predicate=remove_untracked_option,
            clock=self.__clock,
        )
        df_avg = average_rates(df=df)
        df_filtered = filter_rates(
            df=df_avg, max_delivery_price=self.__config.max_delivery_price
        )
        df_rates = select_rates(df_avg=df_avg, df_filtered=df_filtered)

        self.__file_writer.write(filename=rates_filename, data=df_rates)
