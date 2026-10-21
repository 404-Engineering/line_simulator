"""Driver interface. One instance per PLC; the bridge batches all tags per step."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Self


class PlcDriver(ABC):
    @abstractmethod
    def open(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def read(self, tags: list[str]) -> dict[str, Any]:
        """Read many tags in one request. Returns ``{tag: value}``."""

    @abstractmethod
    def write(self, values: dict[str, Any]) -> None:
        """Write many tags in one request."""

    def __enter__(self) -> Self:
        self.open()
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()
