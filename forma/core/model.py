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
        for name, joint in self.joints.items():
            if len(joint) != 3:
                raise ValueError(f"joint '{name}' debe tener 3 coordenadas")

    def total_height(self) -> float:
        return float(sum(self.bone_lengths.values()))


@dataclass
class Muscle:
    """Músculo parametrizado (modelado individual al máximo)."""

    name: str
    origin: str
    insertion: str
    volume: float = 0.0
    length: float = 0.0
    thickness: float = 0.0
    shape: str = "fusiforme"
    pennation_angle: float = 0.0
    fiber_type: str = "mixed"
    max_force: float = 0.0
    origin_point: tuple[float, float, float] = (0.0, 0.0, 0.0)
    insertion_point: tuple[float, float, float] = (0.0, 0.0, 0.0)
    function: str = ""
    innervation: str = ""  # nervio motor
    blood_supply: str = ""  # arteria principal
    fascicles: int = 1  # número de fascículos
    optimal_length: float = 0.0  # longitud óptima (m)

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("el músculo debe tener nombre")
        if self.volume < 0 or self.length < 0 or self.thickness < 0:
            raise ValueError(f"parámetros negativos en músculo {self.name}")
        if self.pennation_angle < 0 or self.pennation_angle > 90:
            raise ValueError(f"ángulo de penación inválido: {self.pennation_angle}")
        if self.max_force < 0:
            raise ValueError(f"fuerza máxima negativa: {self.max_force}")
        if self.fascicles < 1:
            raise ValueError(f"fascicles inválido: {self.fascicles}")
        if self.optimal_length < 0:
            raise ValueError(f"longitud óptima negativa: {self.optimal_length}")


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

    def __post_init__(self) -> None:
        if self.vertex_count < 0:
            raise ValueError("vertex_count no puede ser negativo")


@dataclass
class DigitalTwin:
    """Gemelo digital persistente por persona."""

    person_id: str
    skeleton: Skeleton = field(default_factory=Skeleton)

    def __post_init__(self) -> None:
        if not self.person_id:
            raise ValueError("person_id no puede estar vacío")

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
        if len(set(bone_names)) != len(bone_names):
            raise ValueError("bone_names duplicados")
        if len(set(muscle_names)) != len(muscle_names):
            raise ValueError("muscle_names duplicados")
        if len(set(adipose_regions)) != len(adipose_regions):
            raise ValueError("adipose_regions duplicados")
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
