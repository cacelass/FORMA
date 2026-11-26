"""Puente con Blender (PHASE-1).

Encapsula la interacción con Blender tras la interfaz `BaseBodyProvider`, de
modo que el núcleo anatómico no depende del motor de render. Sin Blender
instalado, el puente opera en modo 'mock' (delega al proveedor base).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from forma.providers.base_body_provider import BaseBodyProvider


class BlenderBridge:
    def __init__(self, provider: BaseBodyProvider, work_dir: Path | None = None) -> None:
        self.provider = provider
        self.work_dir = work_dir or Path(".")

    def load_model(self, path: Path | None = None) -> Any:
        return self.provider.load(path)

    def render_views(self) -> dict[str, Any]:
        return self.provider.render_views()

    def save(self, path: Path) -> None:
        self.provider.save(path)

    def reload(self, path: Path) -> Any:
        return self.provider.reload(path)

    def describe(self) -> dict[str, str]:
        return {
            "bridge": "blender",
            "provider": self.provider.name,
            "mode": "mock" if self.provider.name == "base" else "live",
        }
