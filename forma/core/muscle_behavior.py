"""Comportamiento individual del músculo (modelo de Hill completo)."""

from __future__ import annotations

import math

from forma.core.model import Muscle


class MuscleBehavior:
    """Modelo de músculo individual: fuerza, contracción, activación."""

    def __init__(self, muscle: Muscle, max_force: float | None = None) -> None:
        self.muscle = muscle
        self.max_force = (
            max_force
            if max_force is not None
            else (muscle.max_force if muscle.max_force > 0 else muscle.volume * 10.0)
        )
        self.activation: float = 0.0
        self.current_length: float = muscle.length if muscle.length > 0 else 1.0
        self.velocity: float = 0.0

    @property
    def optimal_length(self) -> float:
        return (
            self.muscle.optimal_length
            if self.muscle.optimal_length > 0
            else (self.muscle.length if self.muscle.length > 0 else 1.0)
        )

    def force_length(self, length: float | None = None) -> float:
        L = length if length is not None else self.current_length
        lopt = self.optimal_length
        return math.exp(-((L - lopt) ** 2) / (2 * (0.1 * lopt) ** 2 + 1e-9))

    def force_velocity(self, velocity: float | None = None) -> float:
        v = velocity if velocity is not None else self.velocity
        if v >= 0:
            return 1.0 / (1.0 + v)
        return 1.0 + 0.5 * abs(v)

    def pennation_factor(self) -> float:
        import math as _m

        return _m.cos(_m.radians(self.muscle.pennation_angle))

    def isometric_force(
        self, activation: float | None = None, length: float | None = None
    ) -> float:
        a = activation if activation is not None else self.activation
        a = max(0.0, min(1.0, a))
        fl = self.force_length(length)
        return a * self.max_force * fl * self.pennation_factor()

    def dynamic_force(
        self,
        activation: float | None = None,
        length: float | None = None,
        velocity: float | None = None,
    ) -> float:
        a = activation if activation is not None else self.activation
        L = length if length is not None else self.current_length
        v = velocity if velocity is not None else self.velocity
        return self.isometric_force(a, L) * self.force_velocity(v)

    def contract(self, activation: float, dt: float = 0.01) -> float:
        """Simula una contracción: actualiza estado y devuelve fuerza."""
        self.activation = max(0.0, min(1.0, activation))
        # acortamiento proporcional a activación
        shortening = self.activation * 0.01 * dt
        self.current_length = max(0.1, self.current_length - shortening)
        self.velocity = -shortening / dt if dt > 0 else 0.0
        return self.dynamic_force()

    def relax(self, dt: float = 0.01) -> None:
        self.activation = max(0.0, self.activation - 0.1 * dt)
        self.current_length = min(self.muscle.length or 1.0, self.current_length + 0.005 * dt)
        self.velocity = 0.0

    def reset(self) -> None:
        self.activation = 0.0
        self.current_length = self.muscle.length if self.muscle.length > 0 else 1.0
        self.velocity = 0.0

    def state(self) -> dict[str, float]:
        return {
            "activation": self.activation,
            "length": self.current_length,
            "velocity": self.velocity,
            "force": self.dynamic_force(),
        }
