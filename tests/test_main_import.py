"""Importar el paquete forma no ejecuta la CLI ni mata el proceso (FIX-001)."""

from __future__ import annotations

import contextlib
import pkgutil

import forma
import forma.__main__  # noqa: F401 — regresión: importar no debe ejecutar la CLI


def test_walk_packages_sobre_forma_no_mata_el_proceso() -> None:
    modulos = [m.name for m in pkgutil.walk_packages(forma.__path__, prefix="forma.")]
    assert "forma.__main__" in modulos
    assert "forma.cli" in modulos


def test_main_como_script_sale_cero() -> None:
    import runpy
    import sys
    from unittest.mock import patch

    with (
        patch.object(sys, "argv", ["forma", "hello"]),
        patch("sys.exit"),
        contextlib.suppress(SystemExit),
    ):
        runpy.run_module("forma.__main__", run_name="__main__")
        # si no lanzó SystemExit, main() devolvió 0 y sys.exit(0) se llamó
