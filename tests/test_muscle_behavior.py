"""Comportamiento individual del músculo."""

from __future__ import annotations

import pytest

from forma.core.anatomy import MUSCLE_CATALOG
from forma.core.model import Muscle
from forma.core.muscle_behavior import MuscleBehavior


def test_force_length_optimo() -> None:
    m = Muscle(name="b", origin="", insertion="", length=1.0, volume=1.0, optimal_length=1.0)
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


def test_contract_relax_reset() -> None:
    m = Muscle(name="b", origin="", insertion="", length=1.0, volume=1.0)
    mb = MuscleBehavior(m, max_force=10.0)
    f = mb.contract(1.0, 0.01)
    assert f >= 0
    mb.relax(0.01)
    mb.reset()
    assert mb.activation == 0.0
    assert mb.state()["force"] >= 0


def test_state() -> None:
    m = Muscle(name="b", origin="", insertion="", length=1.0, volume=1.0)
    mb = MuscleBehavior(m, max_force=10.0)
    st = mb.state()
    assert set(st.keys()) == {"activation", "length", "velocity", "force"}


def test_pennation() -> None:
    m = Muscle(name="b", origin="", insertion="", length=1.0, volume=1.0, pennation_angle=30.0)
    mb = MuscleBehavior(m, max_force=10.0)
    assert 0 < mb.pennation_factor() < 1


def test_cada_musculo_catalogo() -> None:
    for spec in MUSCLE_CATALOG:
        from forma.core.anatomy import BONE_LANDMARKS
        from forma.core.model import Muscle

        m = Muscle(
            name=spec.name,
            origin=spec.origin,
            insertion=spec.insertion,
            volume=spec.volume,
            shape=spec.shape,
            pennation_angle=spec.pennation_angle,
            fiber_type=spec.fiber_type,
            max_force=spec.max_force,
            origin_point=BONE_LANDMARKS.get(spec.origin, (0.0, 0.0, 0.0)),
            insertion_point=BONE_LANDMARKS.get(spec.insertion, (0.0, 0.0, 0.0)),
            function=spec.function,
        )
        mb = MuscleBehavior(m, max_force=m.max_force)
        assert mb.isometric_force(1.0, m.length or 1.0) >= 0
        assert mb.state()["force"] >= 0
