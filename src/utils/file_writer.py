from typing import Protocol, Generic, TypeVar
from pathlib import Path
import pandas as pd

T = TypeVar("T")


class FileWriter(Protocol[T]):
    def file_extension(self) -> str: ...
    def file_exists(self, *, filename: str) -> bool: ...
    def write(self, *, filename: str, data: T) -> None: ...


class PdCsvWriter:
    def __init__(self, *, dir_path: Path) -> None:
        self.__dir_path = dir_path

    def file_extension(self) -> str:
        return ".csv"

    def file_exists(self, *, filename: str) -> bool:
        filepath = self.__dir_path / filename
        return filepath.exists()

    def write(self, *, filename: str, data: pd.DataFrame) -> None:
        if not self.__dir_path.exists():
            self.__dir_path.mkdir()

        filepath = self.__dir_path / filename
        data.to_csv(filepath, index=False)
