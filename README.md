# line_simulator

Physics-based simulator for packaging and filling lines, built in Godot 4. Models conveyors,
sensors, motors, accumulation and bottles, drives them from real or emulated Allen-Bradley
Logix PLCs over EtherNet/IP (pycomm3), and measures throughput, cycle times and bottlenecks
per bottle format. Runs natively on macOS.

## Layout

| Path | What |
|---|---|
| `godot/` | The Godot 4 project. Open this folder in Godot. |
| `godot/core/` | Sim clock, signal bus, bridge client, metrics — line-independent |
| `godot/components/` | Conveyor, photoeye, motor, accumulation table, spawner |
| `godot/products/` | Bottle formats |
| `godot/scenes/lines/` | One scene per line |
| `bridge/` | Python PLC bridge (`pycomm3`) |
| `experiments/` | Recipes and batch runs |
| `config/` | Tag maps and line parameters shared by both sides |
| `plc/` | PLC exports and test programs |
| `docs/` | [Design](docs/DESIGN.md), [phases](docs/phases.md) |
| `runs/` | Batch-run output (ignored) |

## Requirements

- Godot 4.7+ (Jolt physics is built in)
- Python 3.11+ and [uv](https://github.com/astral-sh/uv) for the bridge

## Quick start

```bash
# Simulator
/Applications/Godot.app/Contents/MacOS/Godot --path godot

# Bridge (in another terminal)
cd bridge && uv venv && uv pip install -e ".[dev]"
line-bridge --tagmap ../config/tagmaps/line2.yaml
```

## Status

Phase 0 (spike). See [docs/phases.md](docs/phases.md).
