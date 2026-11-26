"""Modelo paramétrico del gemelo digital humano.

Capas independientes y reemplazables (esqueleto, músculos, adiposo, piel).
El núcleo no depende del motor de render ni de la interfaz.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class Skeleton:
    """Proporciones óseas y articulaciones (normalizadas)."""

    bone_lengths: dict[str, float] = field(default_factory=dict)
    joints: dict[str, tuple[float, float, float]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name, length in self.bone_lengths.items():
            if length < 0:
                raise ValueError(f"longitud ósea negativa: {name}={length}")

    def total_height(self) -> float:
        return float(sum(self.bone_lengths.values()))


@dataclass
class Muscle:
    """Músculo parametrizado."""

    name: str
    origin: str
    insertion: str
    volume: float = 0.0
    length: float = 0.0
    thickness: float = 0.0

    def __post_init__(self) -> None:
        if self.volume < 0 or self.length < 0 or self.thickness < 0:
            raise ValueError(f"parámetros negativos en músculo {self.name}")


@dataclass
class AdiposeLayer:
    """Tejido adiposo subcutáneo regional."""

    regions: dict[str, float] = field(default_factory=dict)  # región -> mm

    def __post_init__(self) -> None:
        for r, v in self.regions.items():
            if v < 0:
                raise ValueError(f"grasa negativa en región {r}")


@dataclass
class Skin:
    """Superficie externa: malla, UV, material."""

    vertex_count: int = 0
    uv: bool = False
    material: str = "skin_default"


@dataclass
class DigitalTwin:
    """Gemelo digital persistente por persona."""

    person_id: str
    skeleton: Skeleton = field(default_factory=Skeleton)
    muscles: dict[str, Muscle] = field(default_factory=dict)
    adipose: AdiposeLayer = field(default_factory=AdiposeLayer)
    skin: Skin = field(default_factory=Skin)
    metadata: dict[str, str] = field(default_factory=dict)

    def muscle_names(self) -> list[str]:
        return sorted(self.muscles.keys())

    def total_muscle_volume(self) -> float:
        return float(sum(m.volume for m in self.muscles.values()))

    def to_vector(self) -> np.ndarray:
        """Vector numérico para optimización: longitudes óseas + volúmenes musculares."""
        parts: list[float] = list(self.skeleton.bone_lengths.values())
        parts += [self.muscles[name].volume for name in sorted(self.muscles)]
        parts += list(self.adipose.regions.values())
        return np.asarray(parts, dtype=float)

    @classmethod
    def from_vector(
        cls,
        person_id: str,
        vec: np.ndarray,
        bone_names: list[str],
        muscle_names: list[str],
        adipose_regions: list[str],
    ) -> DigitalTwin:
        n_b = len(bone_names)
        n_m = len(muscle_names)
        n_a = len(adipose_regions)
        if vec.shape[0] != n_b + n_m + n_a:
            raise ValueError("dimensión del vector no coincide con el modelo")
        sk = Skeleton(bone_lengths={bone_names[i]: float(vec[i]) for i in range(n_b)})
        muscles = {}
        for j, name in enumerate(muscle_names):
            muscles[name] = Muscle(name=name, origin="", insertion="", volume=float(vec[n_b + j]))
        adipose = AdiposeLayer(
            regions={adipose_regions[k]: float(vec[n_b + n_m + k]) for k in range(n_a)}
        )
        return cls(person_id=person_id, skeleton=sk, muscles=muscles, adipose=adipose)
