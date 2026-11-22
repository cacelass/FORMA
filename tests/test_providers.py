"""Abstracción BaseBodyProvider (BASE-001)."""

from __future__ import annotations

import pytest

from forma.providers.base_body_provider import BaseBodyProvider


def test_no_se_puede_instanciar_la_abstraccion() -> None:
    with pytest.raises(TypeError):
        BaseBodyProvider()  # type: ignore[abstract]


def test_subclase_concreta_se_instancia() -> None:
    class Dummy(BaseBodyProvider):
        name = "dummy"

        def load(self, path: object = None) -> object:  # type: ignore[override]
            return "loaded"

        def render_views(self) -> dict[str, object]:  # type: ignore[override]
            return {"front": "x"}

        def save(self, path: object) -> None:  # type: ignore[override]
            return None

        def reload(self, path: object) -> object:  # type: ignore[override]
            return "reloaded"

    p = Dummy()
    assert p.name == "dummy"
    assert p.load() == "loaded"
    assert p.render_views() == {"front": "x"}
    assert p.describe() == {"provider": "dummy"}
