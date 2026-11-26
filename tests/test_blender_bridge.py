"""BlenderBridge (PHASE-1)."""

from __future__ import annotations

from pathlib import Path

import pytest

from forma.blender_bridge import BlenderBridge
from forma.providers.base_body_provider import BaseBodyProvider


class Dummy(BaseBodyProvider):
    name = "dummy"

    def load(self, path=None):
        return "loaded"

    def render_views(self):
        return {"front": "x", "side": "y", "back": "z"}

    def save(self, path):
        return None

    def reload(self, path):
        return "reloaded"


def test_bridge_delega() -> None:
    b = BlenderBridge(Dummy())
    assert b.load_model() == "loaded"
    views = b.render_views()
    assert set(views.keys()) == {"front", "side", "back"}
    b.save(Path("/tmp/x"))
    assert b.reload(Path("/tmp/x")) == "reloaded"
    assert b.describe()["provider"] == "dummy"


def test_bridge_describe_mock() -> None:
    b = BlenderBridge(Dummy())
    assert b.describe()["mode"] == "live"
