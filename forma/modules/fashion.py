"""Módulo de aplicación: fashion (tallas)."""

from __future__ import annotations

from forma.core.model import DigitalTwin


class FashionModule:
    def __init__(self, twin: DigitalTwin) -> None:
        self.twin = twin

    def size_bucket(self) -> str:
        h = self.twin.skeleton.total_height()
        if h < 1.6:
            return "S"
        if h < 1.75:
            return "M"
        return "L"
