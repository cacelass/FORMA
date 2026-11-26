"""Datos anatómicos: esqueleto y músculos con origen/inserción (modelado individual)."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from forma.core.model import DigitalTwin, Muscle, Skeleton

BONE_LANDMARKS: dict[str, tuple[float, float, float]] = {
    "skull": (0.0, 1.75, 0.0),
    "cervical": (0.0, 1.6, 0.0),
    "thoracic": (0.0, 1.35, 0.0),
    "lumbar": (0.0, 1.1, 0.0),
    "pelvis": (0.0, 0.95, 0.0),
    "shoulder_l": (-0.2, 1.45, 0.0),
    "shoulder_r": (0.2, 1.45, 0.0),
    "elbow_l": (-0.35, 1.15, 0.0),
    "elbow_r": (0.35, 1.15, 0.0),
    "wrist_l": (-0.45, 0.95, 0.0),
    "wrist_r": (0.45, 0.95, 0.0),
    "hip_l": (-0.1, 0.9, 0.0),
    "hip_r": (0.1, 0.9, 0.0),
    "knee_l": (-0.12, 0.5, 0.0),
    "knee_r": (0.12, 0.5, 0.0),
    "ankle_l": (-0.12, 0.05, 0.0),
    "ankle_r": (0.12, 0.05, 0.0),
}


@dataclass
class MuscleSpec:
    name: str
    origin: str
    insertion: str
    function: str
    volume: float = 1.0
    shape: str = "fusiforme"
    pennation_angle: float = 0.0
    fiber_type: str = "mixed"
    max_force: float = 0.0
    agonists: list[str] = field(default_factory=list)
    antagonists: list[str] = field(default_factory=list)


MUSCLE_CATALOG: list[MuscleSpec] = [
    MuscleSpec(
        "deltoides",
        "shoulder_r",
        "elbow_r",
        "abducción del hombro",
        0.4,
        "multipennate",
        15.0,
        "mixed",
        40.0,
        agonists=["supraespinoso"],
        antagonists=["dorsal_ancho"],
    ),
    MuscleSpec(
        "pectoral_mayor",
        "shoulder_r",
        "thoracic",
        "aducción/flexión del hombro",
        0.6,
        "fan",
        0.0,
        "mixed",
        60.0,
        antagonists=["dorsal_ancho"],
    ),
    MuscleSpec(
        "biceps_braquial",
        "shoulder_r",
        "elbow_r",
        "flexión del codo y supinación",
        0.25,
        "fusiforme",
        0.0,
        "fast",
        25.0,
        antagonists=["triceps_braquial"],
    ),
    MuscleSpec(
        "triceps_braquial",
        "shoulder_r",
        "elbow_r",
        "extensión del codo",
        0.35,
        "pennate",
        12.0,
        "fast",
        35.0,
        antagonists=["biceps_braquial"],
    ),
    MuscleSpec(
        "recto_abdominal",
        "pelvis",
        "thoracic",
        "flexión del tronco",
        0.3,
        "strap",
        0.0,
        "slow",
        30.0,
        antagonists=["erector_espinal"],
    ),
    MuscleSpec(
        "cuadriceps",
        "hip_r",
        "knee_r",
        "extensión de la rodilla",
        0.8,
        "pennate",
        10.0,
        "mixed",
        80.0,
        antagonists=["isquiotibiales"],
    ),
    MuscleSpec(
        "isquiotibiales",
        "pelvis",
        "knee_r",
        "flexión de la rodilla y extensión de cadera",
        0.5,
        "bipennate",
        15.0,
        "mixed",
        50.0,
        antagonists=["cuadriceps"],
    ),
    MuscleSpec(
        "gastrocnemio",
        "knee_r",
        "ankle_r",
        "flexión plantar",
        0.3,
        "pennate",
        12.0,
        "mixed",
        30.0,
        antagonists=["tibial_anterior"],
    ),
    MuscleSpec(
        "dorsal_ancho",
        "thoracic",
        "shoulder_r",
        "extensión/aducción del hombro",
        0.7,
        "fan",
        0.0,
        "slow",
        70.0,
        antagonists=["pectoral_mayor"],
    ),
    MuscleSpec(
        "trapecio",
        "cervical",
        "shoulder_r",
        "elevación/retracción escapular",
        0.4,
        "triangular",
        0.0,
        "mixed",
        40.0,
    ),
]


def build_skeleton() -> Skeleton:
    bone_lengths = {
        "columna": 0.8,
        "brazo_der": 0.3,
        "antebrazo_der": 0.25,
        "brazo_izq": 0.3,
        "antebrazo_izq": 0.25,
        "muslo_der": 0.4,
        "pierna_der": 0.4,
        "muslo_izq": 0.4,
        "pierna_izq": 0.4,
    }
    sk = Skeleton(bone_lengths=bone_lengths)
    sk.joints = {name: coord for name, coord in BONE_LANDMARKS.items()}
    return sk


def build_twin(person_id: str = "default") -> DigitalTwin:
    sk = build_skeleton()
    muscles: dict[str, Muscle] = {}
    for spec in MUSCLE_CATALOG:
        o_pt = BONE_LANDMARKS.get(spec.origin, (0.0, 0.0, 0.0))
        i_pt = BONE_LANDMARKS.get(spec.insertion, (0.0, 0.0, 0.0))
        muscles[spec.name] = Muscle(
            name=spec.name,
            origin=spec.origin,
            insertion=spec.insertion,
            volume=spec.volume,
            shape=spec.shape,
            pennation_angle=spec.pennation_angle,
            fiber_type=spec.fiber_type,
            max_force=spec.max_force if spec.max_force > 0 else spec.volume * 10.0,
            origin_point=o_pt,
            insertion_point=i_pt,
            function=spec.function,
        )
    return DigitalTwin(person_id=person_id, skeleton=sk, muscles=muscles)


def muscle_force_vector(spec: MuscleSpec) -> np.ndarray:
    o = np.asarray(BONE_LANDMARKS.get(spec.origin, (0, 0, 0)), dtype=float)
    i = np.asarray(BONE_LANDMARKS.get(spec.insertion, (0, 0, 0)), dtype=float)
    v = i - o
    n = np.linalg.norm(v)
    return v / n if n > 0 else np.zeros(3)
