"""Gestor del gemelo digital: reconstruir, editar, guardar, comparar."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from forma.core.model import DigitalTwin
from forma.persistence.store import load_twin, save_twin
from forma.reconstruction.pipeline import ReconstructionPipeline


class TwinManager:
    def __init__(self, storage_dir: str | Path = ".") -> None:
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def reconstruct(self, views: list[Any]) -> DigitalTwin:
        pipe = ReconstructionPipeline()
        result = pipe.fit(views)
        return result.twin  # type: ignore[no-any-return]

    def edit_muscle(self, twin: DigitalTwin, muscle: str, volume: float) -> DigitalTwin:
        if muscle not in twin.muscles:
            raise KeyError(f"músculo desconocido: {muscle}")
        twin.muscles[muscle].volume = volume
        return twin

    def save(self, twin: DigitalTwin, name: str) -> Path:
        path = self.storage_dir / f"{name}.json"
        save_twin(twin, path)
        return path

    def load(self, name: str) -> DigitalTwin:
        path = self.storage_dir / f"{name}.json"
        return load_twin(path)

    def compare(self, a: DigitalTwin, b: DigitalTwin) -> dict[str, float]:
        va = a.to_vector()
        vb = b.to_vector()
        n = min(len(va), len(vb))
        diff = va[:n] - vb[:n]
        return {
            "l2_distance": float(np.linalg.norm(diff)),
            "max_diff": float(np.max(np.abs(diff))) if n else 0.0,
        }

    def list_configs(self) -> list[str]:
        return sorted(p.stem for p in self.storage_dir.glob("*.json"))
