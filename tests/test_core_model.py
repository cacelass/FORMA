"""Núcleo anatómico paramétrico (PHASE-2)."""

from __future__ import annotations

import numpy as np
import pytest

from forma.core.model import AdiposeLayer, DigitalTwin, Muscle, Skeleton


def test_skeleton_valida_longitud_negativa() -> None:
    with pytest.raises(ValueError):
        Skeleton(bone_lengths={"spine": -1.0})


def test_muscle_valida_negativos() -> None:
    with pytest.raises(ValueError):
        Muscle(name="x", origin="a", insertion="b", volume=-1.0)


def test_digital_twin_to_from_vector_roundtrip() -> None:
    sk = Skeleton(bone_lengths={"spine": 1.0, "leg": 2.0})
    muscles = {"biceps": Muscle(name="biceps", origin="o", insertion="i", volume=0.5)}
    adipose = AdiposeLayer(regions={"abdomen": 3.0})
    twin = DigitalTwin(person_id="p1", skeleton=sk, muscles=muscles, adipose=adipose)
    vec = twin.to_vector()
    bone_names = ["spine", "leg"]
    muscle_names = ["biceps"]
    regions = ["abdomen"]
    twin2 = DigitalTwin.from_vector("p1", vec, bone_names, muscle_names, regions)
    assert twin2.skeleton.bone_lengths["spine"] == pytest.approx(1.0)
    assert twin2.muscles["biceps"].volume == pytest.approx(0.5)
    assert twin2.adipose.regions["abdomen"] == pytest.approx(3.0)


def test_from_vector_dimension_mismatch() -> None:
    with pytest.raises(ValueError):
        DigitalTwin.from_vector("p", np.array([1.0]), ["spine"], ["biceps"], ["abd"])


def test_total_muscle_volume() -> None:
    twin = DigitalTwin(
        person_id="p",
        muscles={
            "a": Muscle(name="a", origin="", insertion="", volume=2.0),
            "b": Muscle(name="b", origin="", insertion="", volume=3.0),
        },
    )
    assert twin.total_muscle_volume() == pytest.approx(5.0)


def test_muscle_names() -> None:
    twin = DigitalTwin(
        person_id="p",
        muscles={
            "b": Muscle(name="b", origin="", insertion="", volume=1.0),
            "a": Muscle(name="a", origin="", insertion="", volume=2.0),
        },
    )
    assert twin.muscle_names() == ["a", "b"]


def test_adipose_valida_negativo() -> None:
    with __import__("pytest").raises(ValueError):
        AdiposeLayer(regions={"x": -1.0})
