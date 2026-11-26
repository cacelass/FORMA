"""Superficie y piel (PHASE-4)."""

from __future__ import annotations

import numpy as np
import pytest

from forma.surface.material import SkinMaterial
from forma.surface.mesh import SurfaceMesh
from forma.surface.uv import UVMap


def test_mesh_counts() -> None:
    verts = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=float)
    faces = np.array([[0, 1, 2]])
    m = SurfaceMesh(vertices=verts, faces=faces)
    assert m.vertex_count() == 3
    assert m.face_count() == 1
    assert m.area() > 0


def test_mesh_validaciones() -> None:
    with pytest.raises(ValueError):
        SurfaceMesh(vertices=np.array([[0, 0]]), faces=np.zeros((0, 3), dtype=int))
    with pytest.raises(ValueError):
        SurfaceMesh(vertices=np.array([[0, 0, 0]]), faces=np.array([[0, 1, 2]]))


def test_uv() -> None:
    u = UVMap(coords=np.array([[0.0, 0.0], [1.0, 1.0]]))
    assert u.in_range() is True
    with pytest.raises(ValueError):
        UVMap(coords=np.array([[0.0, 0.0, 0.0]]))


def test_material() -> None:
    m = SkinMaterial()
    assert m.sss is True
    with pytest.raises(ValueError):
        SkinMaterial(roughness=2.0)
    with pytest.raises(ValueError):
        SkinMaterial(color=(1.0, 0.0))
