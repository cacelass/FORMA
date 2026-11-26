"""Persistencia del gemelo (validaciones)."""

from __future__ import annotations

import json
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


def test_load_json_malformado(tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        load_twin(path)


def test_load_person_id_invalido(tmp_path: Path) -> None:
    path = tmp_path / "t.json"
    path.write_text(
        '{"person_id": 123, "skeleton": {"bone_lengths": {}, "joints": {}}, "muscles": {}, "adipose": {"regions": {}}, "skin": {"vertex_count": 0, "uv": false, "material": "x"}, "metadata": {}}',
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_twin(path)


def test_load_joint_longitud(tmp_path: Path) -> None:
    path = tmp_path / "t.json"
    path.write_text(
        '{"person_id": "p", "skeleton": {"bone_lengths": {}, "joints": {"a": [1.0, 2.0]}}, "muscles": {}, "adipose": {"regions": {}}, "skin": {"vertex_count": 0, "uv": false, "material": "x"}, "metadata": {}}',
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_twin(path)


def test_load_metadata_invalida(tmp_path: Path) -> None:
    path = tmp_path / "t.json"
    path.write_text(
        '{"person_id": "p", "skeleton": {"bone_lengths": {}, "joints": {}}, "muscles": {}, "adipose": {"regions": {}}, "skin": {"vertex_count": 0, "uv": false, "material": "x"}, "metadata": "bad"}',
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_twin(path)


def test_save_load_str_path(tmp_path: Path) -> None:
    twin = DigitalTwin(person_id="p")
    path = str(tmp_path / "t.json")
    save_twin(twin, path)
    loaded = load_twin(path)
    assert loaded.person_id == "p"
