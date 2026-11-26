"""Attachment a superficie (proyección al punto más cercano)."""

from __future__ import annotations

import numpy as np


def attach_to_surface(point: np.ndarray, surface_points: np.ndarray) -> np.ndarray:
    point = np.asarray(point, dtype=float)
    surface_points = np.asarray(surface_points, dtype=float)
    if point.shape != (3,):
        raise ValueError("point debe ser (3,)")
    if surface_points.ndim != 2 or surface_points.shape[1] != 3:
        raise ValueError("surface_points debe ser (N,3)")
    if surface_points.shape[0] == 0:
        raise ValueError("surface vacía")
    dists = np.linalg.norm(surface_points - point, axis=1)
    idx = int(np.argmin(dists))
    return surface_points[idx]
