"""Motor de interacción (PHASE-5)."""

from forma.interaction.attachment import attach_to_surface
from forma.interaction.collision import BoundingBox, collides

__all__ = ["BoundingBox", "collides", "attach_to_surface"]
