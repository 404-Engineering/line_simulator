"""Tag map: simulator signal name <-> PLC tag.

Loaded from ``config/tagmaps/<line>.yaml``. See that file for the format.
Direction is from the simulator's point of view: ``input`` signals are sensors
the sim writes to the PLC, ``output`` signals are actuator commands the PLC
writes to the sim.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

import yaml

Direction = Literal["input", "output"]
TagType = Literal["BOOL", "INT", "DINT", "REAL"]


@dataclass(frozen=True)
class PlcConfig:
    name: str
    driver: str  # "logix" for now
    host: str
    slot: int = 0


@dataclass(frozen=True)
class TagBinding:
    signal: str
    plc: str
    tag: str
    type: TagType
    direction: Direction


@dataclass
class TagMap:
    plcs: dict[str, PlcConfig] = field(default_factory=dict)
    bindings: list[TagBinding] = field(default_factory=list)

    def by_direction(self, direction: Direction) -> list[TagBinding]:
        return [b for b in self.bindings if b.direction == direction]

    def for_plc(self, plc: str, direction: Direction) -> list[TagBinding]:
        return [b for b in self.bindings if b.plc == plc and b.direction == direction]


def load(path: str | Path) -> TagMap:
    data = yaml.safe_load(Path(path).read_text())
    tagmap = TagMap()
    for name, cfg in (data.get("plcs") or {}).items():
        tagmap.plcs[name] = PlcConfig(name=name, **cfg)
    for entry in data.get("bindings") or []:
        binding = TagBinding(**entry)
        if binding.plc not in tagmap.plcs:
            raise ValueError(f"binding {binding.signal!r} refers to unknown PLC {binding.plc!r}")
        tagmap.bindings.append(binding)
    _check_unique(tagmap)
    return tagmap


def _check_unique(tagmap: TagMap) -> None:
    seen: set[str] = set()
    for b in tagmap.bindings:
        if b.signal in seen:
            raise ValueError(f"duplicate signal {b.signal!r} in tag map")
        seen.add(b.signal)
