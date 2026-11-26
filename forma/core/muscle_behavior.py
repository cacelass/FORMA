"""Comportamiento individual del músculo (modelo de Hill simplificado)."""

from __future__ import annotations

import math

from forma.core.model import Muscle


class MuscleBehavior:
    """Modelo de músculo: fuerza isométrica, fuerza-longitud, fuerza-velocidad."""

    def __init__(self, muscle: Muscle, max_force: float = 1.0) -> None:
        self.muscle = muscle
        self.max_force = max_force

    def force_length(self, length: float) -> float:
        """Curva fuerza-longitud (gaussiana alrededor de la longitud óptima)."""
        lopt = self.muscle.length if self.muscle.length > 0 else 1.0
        return math.exp(-((length - lopt) ** 2) / (2 * (0.1 * lopt) ** 2 + 1e-9))

    def force_velocity(self, velocity: float) -> float:
        """Curva fuerza-velocidad (concéntrica/excéntrica)."""
        if velocity >= 0:
            return 1.0 / (1.0 + velocity)
        return 1.0 + 0.5 * abs(velocity)

    def isometric_force(self, activation: float, length: float) -> float:
        """Fuerza isométrica = activación * fuerza máxima * fuerza-longitud."""
        a = max(0.0, min(1.0, activation))
        return a * self.max_force * self.force_length(length)

    def dynamic_force(self, activation: float, length: float, velocity: float) -> float:
        return self.isometric_force(activation, length) * self.force_velocity(velocity)
