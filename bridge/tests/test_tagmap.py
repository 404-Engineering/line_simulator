from pathlib import Path

import pytest

from line_bridge import tagmap

CONFIG_DIR = Path(__file__).resolve().parents[2] / "config" / "tagmaps"


def test_example_tagmap_loads():
    tm = tagmap.load(CONFIG_DIR / "line2.yaml")
    assert "lcs" in tm.plcs
    assert tm.by_direction("input")
    assert tm.by_direction("output")


def test_unknown_plc_is_rejected(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        "plcs:\n  a: {driver: logix, host: 10.0.0.1}\n"
        "bindings:\n  - {signal: x, plc: b, tag: X, type: BOOL, direction: input}\n"
    )
    with pytest.raises(ValueError, match="unknown PLC"):
        tagmap.load(bad)


def test_duplicate_signal_is_rejected(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        "plcs:\n  a: {driver: logix, host: 10.0.0.1}\n"
        "bindings:\n"
        "  - {signal: x, plc: a, tag: X, type: BOOL, direction: input}\n"
        "  - {signal: x, plc: a, tag: Y, type: BOOL, direction: input}\n"
    )
    with pytest.raises(ValueError, match="duplicate"):
        tagmap.load(bad)
