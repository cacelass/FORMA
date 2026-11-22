"""Módulo de aplicación: body art (superficie)."""

from __future__ import annotations

from forma.core.model import DigitalTwin


class BodyArtModule:
    def __init__(self, twin: DigitalTwin) -> None:
        self.twin = twin

    def canvas_area(self) -> int:
        return self.twin.skin.vertex_count
