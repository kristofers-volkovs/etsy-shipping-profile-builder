from typing import Protocol, TypeVar
from pathlib import Path


T = TypeVar("T", covariant=True)


class DataLoader(Protocol[T]):
    def load(self, *, path: Path) -> T: ...
