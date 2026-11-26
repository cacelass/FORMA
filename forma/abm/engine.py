"""Motor ABM: cada músculo modelado individualmente."""

from __future__ import annotations

from forma.core.anatomy import build_twin
from forma.core.model import DigitalTwin
from forma.core.muscle_behavior import MuscleBehavior


class AnatomyBasedModel:
    """Modelo basado en anatomía: cada músculo es un agente individual."""

    def __init__(self, twin: DigitalTwin | None = None) -> None:
        self.twin = twin or build_twin()
        self.behaviors: dict[str, MuscleBehavior] = {
            name: MuscleBehavior(m, max_force=m.max_force) for name, m in self.twin.muscles.items()
        }

    def muscle_names(self) -> list[str]:
        return sorted(self.behaviors.keys())

    def activate(
        self,
        muscle_name: str,
        activation: float,
        length: float | None = None,
        velocity: float = 0.0,
    ) -> float:
        if muscle_name not in self.behaviors:
            raise KeyError(f"músculo desconocido: {muscle_name}")
        mb = self.behaviors[muscle_name]
        L = length if length is not None else mb.current_length
        return mb.dynamic_force(activation, L, velocity)

    def contract(self, muscle_name: str, activation: float, dt: float = 0.01) -> float:
        if muscle_name not in self.behaviors:
            raise KeyError(f"músculo desconocido: {muscle_name}")
        return self.behaviors[muscle_name].contract(activation, dt)

    def relax(self, muscle_name: str, dt: float = 0.01) -> None:
        if muscle_name not in self.behaviors:
            raise KeyError(f"músculo desconocido: {muscle_name}")
        self.behaviors[muscle_name].relax(dt)

    def reset(self, muscle_name: str | None = None) -> None:
        if muscle_name is None:
            for mb in self.behaviors.values():
                mb.reset()
        else:
            if muscle_name not in self.behaviors:
                raise KeyError(f"músculo desconocido: {muscle_name}")
            self.behaviors[muscle_name].reset()

    def total_force(
        self, activations: dict[str, float], lengths: dict[str, float] | None = None
    ) -> float:
        lengths = lengths or {}
        total = 0.0
        for name, act in activations.items():
            L = lengths.get(name)
            total += self.activate(name, act, L)
        return total

    def agonist_antagonist_balance(self, agonist: str, antagonist: str, activation: float) -> float:
        f_ag = self.activate(agonist, activation)
        f_ant = self.activate(antagonist, activation * 0.3)
        return f_ag - f_ant

    def state(self, muscle_name: str | None = None) -> dict:
        if muscle_name is None:
            return {name: mb.state() for name, mb in self.behaviors.items()}
        if muscle_name not in self.behaviors:
            raise KeyError(f"músculo desconocido: {muscle_name}")
        return self.behaviors[muscle_name].state()

    def simulate(
        self, activations: dict[str, float], steps: int = 10, dt: float = 0.01
    ) -> list[dict]:
        """Simula N pasos de contracción para los músculos activados."""
        history = []
        for _ in range(steps):
            for name, act in activations.items():
                self.contract(name, act, dt)
            history.append(self.state())
        return history
