"""Módulo de aplicación: fitness."""

from __future__ import annotations

from forma.core.model import DigitalTwin


class FitnessModule:
    def __init__(self, twin: DigitalTwin) -> None:
        self.twin = twin

    def hypertrophy_score(self) -> float:
        return self.twin.total_muscle_volume()

    def bmi_estimate(self, height_m: float) -> float:
        import math

        if not math.isfinite(height_m) or height_m <= 0:
            raise ValueError("altura inválida")
        mass = self.twin.total_muscle_volume() * 10.0 + 50.0
        return mass / (height_m**2)
