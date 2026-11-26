"""Modelo basado en anatomía (ABM) — cada músculo individual."""

from __future__ import annotations

import pytest

from forma.abm.engine import AnatomyBasedModel


def test_muscle_names() -> None:
    abm = AnatomyBasedModel()
    names = abm.muscle_names()
    assert len(names) == 10
    assert "deltoides" in names


def test_activate_cada_musculo() -> None:
    abm = AnatomyBasedModel()
    for name in abm.muscle_names():
        f = abm.activate(name, 0.8, 1.0)
        assert f >= 0


def test_contract_cada_musculo() -> None:
    abm = AnatomyBasedModel()
    for name in abm.muscle_names():
        f = abm.contract(name, 0.5, 0.01)
        assert f >= 0


def test_total_force() -> None:
    abm = AnatomyBasedModel()
    total = abm.total_force(
        {"biceps_braquial": 1.0, "triceps_braquial": 0.5}, {"biceps_braquial": 1.0}
    )
    assert total >= 0


def test_balance() -> None:
    abm = AnatomyBasedModel()
    bal = abm.agonist_antagonist_balance("biceps_braquial", "triceps_braquial", 0.8)
    assert isinstance(bal, float)


def test_musculo_desconocido() -> None:
    abm = AnatomyBasedModel()
    with pytest.raises(KeyError):
        abm.activate("noexiste", 1.0, 1.0)
    with pytest.raises(KeyError):
        abm.contract("noexiste", 1.0)
    with pytest.raises(KeyError):
        abm.relax("noexiste")


def test_state_por_musculo() -> None:
    abm = AnatomyBasedModel()
    st = abm.state("biceps_braquial")
    assert set(st.keys()) == {"activation", "length", "velocity", "force"}


def test_state_todos() -> None:
    abm = AnatomyBasedModel()
    st = abm.state()
    assert len(st) == 10


def test_reset() -> None:
    abm = AnatomyBasedModel()
    abm.contract("biceps_braquial", 1.0)
    abm.reset("biceps_braquial")
    assert abm.state("biceps_braquial")["activation"] == 0.0
    abm.reset()
    for name in abm.muscle_names():
        assert abm.state(name)["activation"] == 0.0


def test_simulate() -> None:
    abm = AnatomyBasedModel()
    hist = abm.simulate({"biceps_braquial": 0.8}, steps=5, dt=0.01)
    assert len(hist) == 5
    assert "biceps_braquial" in hist[-1]


def test_relax() -> None:
    abm = AnatomyBasedModel()
    abm.contract("biceps_braquial", 1.0)
    abm.relax("biceps_braquial")
    assert abm.state("biceps_braquial")["activation"] <= 1.0
