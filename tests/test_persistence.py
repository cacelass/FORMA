"""Persistencia del gemelo (PHASE-? / mejora)."""

from __future__ import annotations

from pathlib import Path

import pytest

from forma.core.model import DigitalTwin, Muscle, Skeleton
from forma.persistence.store import load_twin, save_twin


def test_save_load_roundtrip(tmp_path: Path) -> None:
    twin = DigitalTwin(
        person_id="p1",
        skeleton=Skeleton(bone_lengths={"spine": 1.5}),
        muscles={"b": Muscle(name="b", origin="o", insertion="i", volume=1.0)},
    )
    path = tmp_path / "twin.json"
    save_twin(twin, path)
    loaded = load_twin(path)
    assert loaded.person_id == "p1"
    assert loaded.skeleton.bone_lengths["spine"] == pytest.approx(1.5)
    assert loaded.muscles["b"].volume == pytest.approx(1.0)
