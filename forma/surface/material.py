"""Material de piel."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SkinMaterial:
    name: str = "skin_default"
    color: tuple[float, float, float] = (0.8, 0.6, 0.5)
    roughness: float = 0.5
    sss: bool = True

    def __post_init__(self) -> None:
        if not (0 <= self.roughness <= 1):
            raise ValueError("roughness debe estar en [0,1]")
        if len(self.color) != 3:
            raise ValueError("color debe tener 3 componentes")
