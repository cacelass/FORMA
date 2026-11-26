"""Motor ABM: simula contracción muscular individual."""

from __future__ import annotations

from forma.core.anatomy import build_twin
from forma.core.model import DigitalTwin
from forma.core.muscle_behavior import MuscleBehavior


class AnatomyBasedModel:
    def __init__(self, twin: DigitalTwin | None = None) -> None:
        self.twin = twin or build_twin()
        self.behaviors: dict[str, MuscleBehavior] = {
            name: MuscleBehavior(m, max_force=m.volume * 10.0)
            for name, m in self.twin.muscles.items()
        }

    def activate(
        self, muscle_name: str, activation: float, length: float, velocity: float = 0.0
    ) -> float:
        if muscle_name not in self.behaviors:
            raise KeyError(f"músculo desconocido: {muscle_name}")
        return self.behaviors[muscle_name].dynamic_force(activation, length, velocity)

    def total_force(self, activations: dict[str, float], lengths: dict[str, float]) -> float:
        total = 0.0
        for name, act in activations.items():
            L = lengths.get(name, self.twin.muscles[name].length or 1.0)
            total += self.activate(name, act, L)
        return total

    def agonist_antagonist_balance(self, agonist: str, antagonist: str, activation: float) -> float:
        f_ag = self.activate(agonist, activation, self.twin.muscles[agonist].length or 1.0)
        f_ant = self.activate(
            antagonist, activation * 0.3, self.twin.muscles[antagonist].length or 1.0
        )
        return f_ag - f_ant
