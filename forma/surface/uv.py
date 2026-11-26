"""Mapeo UV."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class UVMap:
    coords: np.ndarray

    def __post_init__(self) -> None:
        self.coords = np.asarray(self.coords, dtype=float)
        if self.coords.ndim != 2 or self.coords.shape[1] != 2:
            raise ValueError("coords debe ser (N,2)")

    def in_range(self) -> bool:
        return bool(np.all(self.coords >= 0) and np.all(self.coords <= 1))
