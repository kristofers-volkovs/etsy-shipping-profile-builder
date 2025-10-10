from typing import Protocol


class FilenameComposer(Protocol):
    def compose_filename(self, *, name: str, extension: str) -> str: ...


class RatesFilenameComposer:
    def compose_filename(self, *, name: str, extension: str) -> str:
        return name + "_rates" + extension
