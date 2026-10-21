# Phases

| # | Phase | Done when |
|---|---|---|
| 0 | Spike | One conveyor, bottles ride it without jitter, one photoeye; bridge reads/writes one tag on a Logix controller (Echo or bench unit) |
| 1 | Core components | Conveyor, photoeye, motor, accumulation table, bottle spawner with format parameter; fixed-step sim; line saved/loaded as a scene |
| 2 | PLC I/O | Tag map in config; bridge exchanges all I/O per step for several PLCs; latency measured |
| 3 | Metrics and batch runs | Throughput, cycle time per station, blocked/starved time, buffer occupancy; `run_batch.py` runs N simulated minutes per recipe; CSV out |
| 4 | Scan meshes | Scanned building mesh as backdrop; equipment rebuilt from primitives with proper colliders |
| 5 | Line 2 twin | Depalletizer → filler → … modelled; validated against measured line numbers |
| 6 | *Stretch* EtherNet/IP adapter | Appear to the PLC as remote I/O for scan-synchronous timing |
| 7 | *Stretch* Format changeover | Guide rails, format parts and changeover times as scenarios |

Targets: bottle physics stable at ≥ 100 Hz with ≥ 500 bottles; PLC round-trip ≤ 20 ms polling;
sim throughput within ±5 % of the real line on a validated stretch.
