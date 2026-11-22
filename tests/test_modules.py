"""Módulos de aplicación (PHASE-6)."""

from __future__ import annotations

import pytest

from forma.core.model import DigitalTwin, Muscle, Skin
from forma.modules.body_art import BodyArtModule
from forma.modules.fashion import FashionModule
from forma.modules.fitness import FitnessModule


def _twin() -> DigitalTwin:
    return DigitalTwin(
        person_id="p",
        skeleton=__import__("forma.core.model", fromlist=["Skeleton"]).Skeleton(bone_lengths={"leg": 1.7}),
        muscles={"b": Muscle(name="b", origin="", insertion="", volume=2.0)},
        skin=Skin(vertex_count=1000),
    )


def test_fitness_hypertrophy() -> None:
    assert FitnessModule(_twin()).hypertrophy_score() == pytest.approx(2.0)


def test_fitness_bmi_invalida() -> None:
    with pytest.raises(ValueError):
        FitnessModule(_twin()).bmi_estimate(0.0)


def test_fashion_size() -> None:
    assert FashionModule(_twin()).size_bucket() in {"S", "M", "L"}


def test_body_art_canvas() -> None:
    assert BodyArtModule(_twin()).canvas_area() == 1000
