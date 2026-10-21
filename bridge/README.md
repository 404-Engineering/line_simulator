# line-bridge

Python sidecar that connects the Godot simulation to PLCs. Each step it receives the
simulator's input signals over UDP, writes them to the PLC tags named in the tag map,
reads the PLC's output tags, and sends those back as output signals.

Runs wherever the PLC is reachable: on the Mac for bench hardware, or on the Windows PC
next to FactoryTalk Logix Echo.

```bash
cd bridge
uv venv && uv pip install -e ".[dev]"
line-bridge --tagmap ../config/tagmaps/line2.yaml
```

Run the tests with `uv run pytest`.
