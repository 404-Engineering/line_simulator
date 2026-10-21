"""PLC drivers. ``make_driver`` picks one from a ``PlcConfig``."""

from __future__ import annotations

from ..tagmap import PlcConfig
from .base import PlcDriver


def make_driver(cfg: PlcConfig) -> PlcDriver:
    if cfg.driver == "logix":
        from .logix import LogixDriver

        return LogixDriver(cfg)
    raise ValueError(f"unknown PLC driver {cfg.driver!r}")


__all__ = ["PlcDriver", "make_driver"]
