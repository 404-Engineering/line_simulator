# Line Simulator — Design

## 1. Purpose

A physics-based simulator for packaging and filling lines, scoped to what one line needs:
Allen-Bradley Logix PLCs over EtherNet/IP, conveyors, sensors, motors, accumulation and
bottles. Native on macOS. Built so the Godot side is reusable across lines and the PLC side
can run next to the controllers.

## 2. Architecture

```
 ┌───────────────────────────┐   UDP, 1 msg/step   ┌──────────────────┐  EtherNet/IP  ┌─────────┐
 │ Godot 4 (godot/)          │ ───── inputs ─────▶ │ bridge/ (Python) │ ───────────▶ │ PLC(s)  │
 │  SimClock · SignalBus     │ ◀──── outputs ───── │  pycomm3 drivers │ ◀─────────── │ or Echo │
 │  components · Metrics     │                     └──────────────────┘               └─────────┘
 └───────────────────────────┘
          ▲  recipes, --line/--recipe/--out
 ┌───────────────────────────┐
 │ experiments/run_batch.py  │ → runs/*.csv
 └───────────────────────────┘
```

- **SimClock** — fixed step at 100 Hz, deterministic, seeded RNG. No wall-clock reads.
- **SignalBus** — named signals (`station.signal`), typed by direction. The only thing
  components and the bridge share.
- **Components** — `components/<name>/`: scene + script. Register their signals on
  `_ready()`, read outputs and write inputs on each `SimClock.stepped`.
- **Metrics** — counts, blocked/starved time per station → CSV.
- **Bridge** — maps signal names to PLC tags from `config/tagmaps/`, one driver per PLC,
  batched read/write per step. Optional: a scripted controller can drive the bus directly.

## 3. Godot ↔ bridge protocol

Datagrams, JSON, localhost.

| Direction | Port | Payload |
|---|---|---|
| Godot → bridge | 7401 | `{"tick": N, "inputs": {"name": value, …}}` |
| bridge → Godot | 7402 | `{"tick": N, "outputs": {"name": value, …}}` |

Godot sends inputs after each physics step and drains any outputs that have arrived.
There is no step lock: the sim does not wait for the PLC. Phase 2 measures the resulting
latency; if it matters, add a lock-step mode (Godot waits for the matching tick) and/or a
binary payload.

## 4. Determinism

- Fixed timestep; Jolt physics; all randomness from `SimClock.rng`.
- PLC I/O is inherently asynchronous. For reproducible *analysis* runs, use a scripted
  controller; use real PLCs for *commissioning* runs.

## 5. Open decisions

- GDScript vs C# for components (scaffolded in GDScript).
- Polling tags vs appearing as EtherNet/IP remote I/O (OpENer) for scan-synchronous timing.
- Where the bridge runs (Mac on the bench vs Windows PC next to Logix Echo).
- How deeply to model the filler/capper vs a timed black box.

## 6. Phases

See `phases.md`.
