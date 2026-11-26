"""Geometría de superficie (malla)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

import numpy as np


@dataclass
class SurfaceMesh:
    vertices: np.ndarray = field(default_factory=lambda: np.zeros((0, 3)))
    faces: np.ndarray = field(default_factory=lambda: np.zeros((0, 3), dtype=int))

    def __post_init__(self) -> None:
        self.vertices = np.asarray(self.vertices, dtype=float)
        self.faces = np.asarray(self.faces, dtype=int)
        if self.vertices.ndim != 2 or self.vertices.shape[1] != 3:
            raise ValueError("vertices debe ser (N,3)")
        if self.faces.ndim != 2 or self.faces.shape[1] != 3:
            raise ValueError("faces debe ser (M,3)")
        if self.faces.size and self.faces.max() >= len(self.vertices):
            raise ValueError("índice de face fuera de rango")

    def vertex_count(self) -> int:
        return int(self.vertices.shape[0])

    def face_count(self) -> int:
        return int(self.faces.shape[0])

    def area(self) -> float:
        if self.faces.size == 0:
            return 0.0
        a = self.vertices[self.faces[:, 0]]
        b = self.vertices[self.faces[:, 1]]
        c = self.vertices[self.faces[:, 2]]
        return float(0.5 * np.sum(np.linalg.cross(b - a, c - a), axis=1).__abs__().sum()) if False else float(0.5 * np.sum(np.abs(np.cross(b - a, c - a)), axis=1).sum())
