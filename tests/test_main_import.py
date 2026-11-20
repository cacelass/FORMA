"""Importar el paquete forma no ejecuta la CLI ni mata el proceso (FIX-001)."""

from __future__ import annotations

import pkgutil

import forma
import forma.__main__  # noqa: F401 — regresión: importar no debe ejecutar la CLI


def test_walk_packages_sobre_forma_no_mata_el_proceso() -> None:
    modulos = [m.name for m in pkgutil.walk_packages(forma.__path__, prefix="forma.")]
    assert "forma.__main__" in modulos
    assert "forma.cli" in modulos