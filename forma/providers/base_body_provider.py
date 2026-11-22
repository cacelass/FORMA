"""Abstracción de proveedor de cuerpo base (BASE-001).

Encapsula la dependencia del motor/malla base (SMPL-X, MakeHuman, MB-Lab,
Blender-native, ...) para que el núcleo anatómico no dependa de una
implementación concreta.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseBodyProvider(ABC):
    """Contrato mínimo que todo proveedor de cuerpo base debe cumplir."""

    name: str = "base"

    @abstractmethod
    def load(self, path: Path | None = None) -> Any:
        """Carga el modelo base y devuelve su handle interno."""

    @abstractmethod
    def render_views(self) -> dict[str, Any]:
        """Renderiza vistas (frontal/lateral/posterior) y devuelve rutas/bytes."""

    @abstractmethod
    def save(self, path: Path) -> None:
        """Persiste el modelo base en `path`."""

    @abstractmethod
    def reload(self, path: Path) -> Any:
        """Recarga un modelo base previamente guardado."""

    def describe(self) -> dict[str, str]:
        return {"provider": self.name}
