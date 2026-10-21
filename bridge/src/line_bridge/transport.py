"""UDP link to Godot. Mirrors ``godot/core/bridge_client.gd``.

Godot -> bridge: ``{"tick": N, "inputs": {name: value}}``
bridge -> Godot: ``{"tick": N, "outputs": {name: value}}``
"""

from __future__ import annotations

import json
import socket
from typing import Any

GODOT_SEND_PORT = 7401  # Godot sends here; the bridge listens
GODOT_LISTEN_PORT = 7402  # Godot listens here; the bridge sends


class GodotLink:
    def __init__(self, host: str = "127.0.0.1", listen_port: int = GODOT_SEND_PORT,
                 send_port: int = GODOT_LISTEN_PORT, timeout: float = 1.0) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((host, listen_port))
        self._sock.settimeout(timeout)
        self._dest = (host, send_port)

    def receive_inputs(self) -> tuple[int, dict[str, Any]] | None:
        """Block for the next step's inputs. ``None`` on timeout."""
        try:
            data, _ = self._sock.recvfrom(65535)
        except TimeoutError:
            return None
        msg = json.loads(data)
        return int(msg["tick"]), dict(msg.get("inputs", {}))

    def send_outputs(self, tick: int, outputs: dict[str, Any]) -> None:
        self._sock.sendto(json.dumps({"tick": tick, "outputs": outputs}).encode(), self._dest)

    def close(self) -> None:
        self._sock.close()
