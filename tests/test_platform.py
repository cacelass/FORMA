"""Interfaz de plataforma (PHASE-7)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from forma.platform.config import ConfigManager
from forma.platform.export import export_json


def test_config_roundtrip(tmp_path: Path) -> None:
    cm = ConfigManager(tmp_path / "cfg.json")
    assert cm.load() == {}
    cm.set("x", 5)
    assert cm.get("x") == 5
    cm.save({"a": 1})
    assert cm.load() == {"a": 1}


def test_config_invalido(tmp_path: Path) -> None:
    p = tmp_path / "cfg.json"
    p.write_text("[1,2]", encoding="utf-8")
    with pytest.raises(ValueError):
        ConfigManager(p).load()


def test_export_json(tmp_path: Path) -> None:
    path = tmp_path / "out.json"
    export_json({"k": "v"}, path)
    assert json.loads(path.read_text()) == {"k": "v"}


def test_config_set_invalido(tmp_path: Path) -> None:
    cm = ConfigManager(tmp_path / "c.json")
    with pytest.raises(ValueError):
        cm.save("bad")  # type: ignore[arg-type]
