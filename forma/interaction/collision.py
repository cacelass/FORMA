"""Colisión (bounding boxes)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class BoundingBox:
    min: np.ndarray
    max: np.ndarray

    def __post_init__(self) -> None:
        self.min = np.asarray(self.min, dtype=float)
        self.max = np.asarray(self.max, dtype=float)
        if self.min.shape != (3,) or self.max.shape != (3,):
            raise ValueError("min/max deben ser (3,)")
        if np.any(self.max < self.min):
            raise ValueError("max debe ser >= min")


def collides(a: BoundingBox, b: BoundingBox) -> bool:
    return bool(np.all(a.min <= b.max) and np.all(b.min <= a.max))
