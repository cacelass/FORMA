"""Núcleo anatómico de FORMA (capas independientes)."""

from forma.core.model import AdiposeLayer, DigitalTwin, Muscle, Skeleton, Skin

__all__ = [
    "MuscleBehavior",
    "AdiposeLayer",
    "DigitalTwin",
    "Muscle",
    "Skeleton",
    "Skin",
    "MUSCLE_CATALOG",
    "MuscleSpec",
    "build_skeleton",
    "build_twin",
    "muscle_force_vector",
]
