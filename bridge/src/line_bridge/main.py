"""Bridge loop: Godot inputs -> PLC tags; PLC tags -> Godot outputs, once per step."""

from __future__ import annotations

import argparse
import logging
import time

from . import tagmap as tagmap_mod
from .plc import make_driver
from .transport import GodotLink

log = logging.getLogger("line_bridge")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Line Simulator PLC bridge")
    parser.add_argument("--tagmap", required=True, help="path to config/tagmaps/<line>.yaml")
    parser.add_argument("--host", default="127.0.0.1", help="Godot host")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")

    tm = tagmap_mod.load(args.tagmap)
    drivers = {name: make_driver(cfg) for name, cfg in tm.plcs.items()}
    for d in drivers.values():
        d.open()
    log.info("connected to %d PLC(s): %s", len(drivers), ", ".join(drivers))

    link = GodotLink(host=args.host)
    log.info("waiting for Godot on UDP %s", args.host)
    try:
        _loop(tm, drivers, link)
    except KeyboardInterrupt:
        pass
    finally:
        link.close()
        for d in drivers.values():
            d.close()
    return 0


def _loop(tm: tagmap_mod.TagMap, drivers: dict, link: GodotLink) -> None:
    inputs_by_plc = {name: tm.for_plc(name, "input") for name in drivers}
    outputs_by_plc = {name: tm.for_plc(name, "output") for name in drivers}
    while True:
        step = link.receive_inputs()
        if step is None:
            continue
        tick, inputs = step
        t0 = time.perf_counter()
        for name, driver in drivers.items():
            to_write = {b.tag: inputs[b.signal] for b in inputs_by_plc[name] if b.signal in inputs}
            driver.write(to_write)
        outputs: dict = {}
        for name, driver in drivers.items():
            bindings = outputs_by_plc[name]
            values = driver.read([b.tag for b in bindings])
            for b in bindings:
                outputs[b.signal] = values[b.tag]
        link.send_outputs(tick, outputs)
        log.debug("tick %d round-trip %.1f ms", tick, (time.perf_counter() - t0) * 1000)


if __name__ == "__main__":
    raise SystemExit(main())
