# plc/

PLC-side artefacts.

- `exports/` — L5X and controller tag CSV exports, used to generate `config/tagmaps/`.
- `test_programs/` — small Logix programs for Phase 0/2 bridge testing.

Only commit exports from the real line with the plant's permission. Until then, keep
them here locally and add the paths to `.git/info/exclude`.
