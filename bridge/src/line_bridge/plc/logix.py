"""Allen-Bradley Logix (ControlLogix / CompactLogix / Logix Echo) via pycomm3."""

from __future__ import annotations

from typing import Any

from pycomm3 import LogixDriver as _Pycomm3Logix

from ..tagmap import PlcConfig
from .base import PlcDriver


class LogixDriver(PlcDriver):
    def __init__(self, cfg: PlcConfig) -> None:
        self.cfg = cfg
        self._plc: _Pycomm3Logix | None = None

    def open(self) -> None:
        # pycomm3 path syntax: "host/slot"
        self._plc = _Pycomm3Logix(f"{self.cfg.host}/{self.cfg.slot}")
        self._plc.open()

    def close(self) -> None:
        if self._plc is not None:
            self._plc.close()
            self._plc = None

    def read(self, tags: list[str]) -> dict[str, Any]:
        assert self._plc is not None, "driver not open"
        if not tags:
            return {}
        results = self._plc.read(*tags)
        if not isinstance(results, list):
            results = [results]
        out: dict[str, Any] = {}
        for r in results:
            if r.error:
                raise RuntimeError(f"{self.cfg.name}: read {r.tag!r} failed: {r.error}")
            out[r.tag] = r.value
        return out

    def write(self, values: dict[str, Any]) -> None:
        assert self._plc is not None, "driver not open"
        if not values:
            return
        results = self._plc.write(*values.items())
        if not isinstance(results, list):
            results = [results]
        for r in results:
            if r.error:
                raise RuntimeError(f"{self.cfg.name}: write {r.tag!r} failed: {r.error}")
