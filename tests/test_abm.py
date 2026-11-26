"""Modelo basado en anatomía (ABM)."""

from __future__ import annotations

import pytest

from forma.abm.engine import AnatomyBasedModel


def test_activate() -> None:
    abm = AnatomyBasedModel()
    f = abm.activate("biceps_braquial", 1.0, 1.0)
    assert f >= 0


def test_total_force() -> None:
    abm = AnatomyBasedModel()
    total = abm.total_force({"biceps_braquial": 1.0}, {"biceps_braquial": 1.0})
    assert total >= 0


def test_balance() -> None:
    abm = AnatomyBasedModel()
    bal = abm.agonist_antagonist_balance("biceps_braquial", "triceps_braquial", 0.8)
    assert isinstance(bal, float)


def test_musculo_desconocido() -> None:
    abm = AnatomyBasedModel()
    with pytest.raises(KeyError):
        abm.activate("noexiste", 1.0, 1.0)
