"""Comportamiento individual del músculo."""

from __future__ import annotations

import pytest

from forma.core.model import Muscle
from forma.core.muscle_behavior import MuscleBehavior


def test_force_length_optimo() -> None:
    m = Muscle(name="b", origin="", insertion="", length=1.0, volume=1.0)
    mb = MuscleBehavior(m, max_force=10.0)
    assert mb.force_length(1.0) == pytest.approx(1.0, abs=1e-6)


def test_isometric_force() -> None:
    m = Muscle(name="b", origin="", insertion="", length=1.0, volume=1.0)
    mb = MuscleBehavior(m, max_force=10.0)
    f = mb.isometric_force(1.0, 1.0)
    assert f > 0
    assert mb.isometric_force(0.0, 1.0) == 0.0


def test_dynamic_force() -> None:
    m = Muscle(name="b", origin="", insertion="", length=1.0, volume=1.0)
    mb = MuscleBehavior(m, max_force=10.0)
    f = mb.dynamic_force(1.0, 1.0, 0.0)
    assert f > 0


def test_force_velocity() -> None:
    m = Muscle(name="b", origin="", insertion="", length=1.0, volume=1.0)
    mb = MuscleBehavior(m, max_force=10.0)
    assert mb.force_velocity(0) == 1.0
