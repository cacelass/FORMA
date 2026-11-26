"""Anatomía (modelado por músculo)."""

from __future__ import annotations

import numpy as np

from forma.core.anatomy import MUSCLE_CATALOG, build_skeleton, build_twin, muscle_force_vector


def test_catalog_no_vacio() -> None:
    assert len(MUSCLE_CATALOG) >= 10


def test_build_skeleton() -> None:
    sk = build_skeleton()
    assert sk.total_height() > 0
    assert "pelvis" in sk.joints


def test_build_twin() -> None:
    twin = build_twin("p1")
    assert twin.person_id == "p1"
    assert "deltoides" in twin.muscles
    assert twin.total_muscle_volume() > 0


def test_muscle_force_vector() -> None:
    spec = MUSCLE_CATALOG[0]
    v = muscle_force_vector(spec)
    assert v.shape == (3,)
    assert abs(np.linalg.norm(v) - 1.0) < 1e-9 or np.linalg.norm(v) == 0
