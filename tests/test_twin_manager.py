"""Gestor del gemelo digital (MVP-001)."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from forma.twin.manager import TwinManager


def test_reconstruct_edit_save_load(tmp_path: Path) -> None:
    tm = TwinManager(tmp_path)
    twin = tm.reconstruct([__import__("numpy").zeros((10, 10))])
    assert twin.person_id == "default"
    tm.edit_muscle(twin, "biceps_braquial", 5.0)
    assert twin.muscles["biceps_braquial"].volume == 5.0
    path = tm.save(twin, "cfg1")
    assert path.exists()
    loaded = tm.load("cfg1")
    assert loaded.muscles["biceps_braquial"].volume == 5.0


def test_edit_musculo_desconocido(tmp_path: Path) -> None:
    tm = TwinManager(tmp_path)
    twin = tm.reconstruct([np.zeros((10, 10))])
    with __import__("pytest").raises(KeyError):
        tm.edit_muscle(twin, "noexiste", 1.0)


def test_compare() -> None:
    tm = TwinManager("/tmp")
    a = tm.reconstruct([np.zeros((10, 10))])
    b = tm.reconstruct([np.zeros((10, 10))])
    tm.edit_muscle(b, "biceps_braquial", 99.0)
    d = tm.compare(a, b)
    assert d["l2_distance"] > 0


def test_list_configs(tmp_path: Path) -> None:
    tm = TwinManager(tmp_path)
    twin = tm.reconstruct([np.zeros((10, 10))])
    tm.save(twin, "x")
    assert "x" in tm.list_configs()
