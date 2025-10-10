from typing import Protocol, Iterable
from pathlib import Path


class DirIterator(Protocol):
    def iter_dir(self) -> Iterable[Path]: ...


class DirFileIterator:
    def __init__(self, *, dir_path: Path, glob: str = "*.csv") -> None:
        self.__dir_path = dir_path
        self.__glob = glob

    def iter_dir(self) -> Iterable[Path]:
        for path in sorted(self.__dir_path.glob(self.__glob)):
            if not path.is_file():
                continue
            yield path
