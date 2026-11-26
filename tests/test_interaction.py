"""Motor de interacción (PHASE-5)."""

from __future__ import annotations

import numpy as np
import pytest

from forma.interaction.attachment import attach_to_surface
from forma.interaction.collision import BoundingBox, collides


def test_collides() -> None:
    a = BoundingBox(min=np.array([0, 0, 0]), max=np.array([1, 1, 1]))
    b = BoundingBox(min=np.array([0.5, 0.5, 0.5]), max=np.array([2, 2, 2]))
    assert collides(a, b) is True
    c = BoundingBox(min=np.array([5, 5, 5]), max=np.array([6, 6, 6]))
    assert collides(a, c) is False


def test_bbox_validaciones() -> None:
    with pytest.raises(ValueError):
        BoundingBox(min=np.array([0, 0]), max=np.array([1, 1, 1]))
    with pytest.raises(ValueError):
        BoundingBox(min=np.array([2, 2, 2]), max=np.array([1, 1, 1]))


def test_attach() -> None:
    surf = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=float)
    p = np.array([0.1, 0.1, 0.0])
    r = attach_to_surface(p, surf)
    assert r.shape == (3,)
    with pytest.raises(ValueError):
        attach_to_surface(np.array([0, 0]), surf)
    with pytest.raises(ValueError):
        attach_to_surface(p, np.zeros((0, 3)))
