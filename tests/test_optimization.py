"""Motor de optimización (OPT-001)."""

from __future__ import annotations

import numpy as np

from forma.optimization.engine import (
    OptimizationResult,
    estimate_uncertainty,
    gradient_descent,
    l2_loss,
    nelder_mead,
    validate,
)


def test_l2_loss_cero_si_iguales() -> None:
    a = np.array([1.0, 2.0, 3.0])
    assert l2_loss(a, a) == 0.0


def test_l2_loss_formas_distintas() -> None:
    with __import__("pytest").raises(ValueError):
        l2_loss(np.array([1.0]), np.array([1.0, 2.0]))


def test_gradient_descent_minimiza_cuadratica() -> None:
    def f(x: np.ndarray) -> float:
        return float(np.sum(x**2))

    def g(x: np.ndarray) -> np.ndarray:
        return 2 * x

    res = gradient_descent(f, g, np.array([5.0, -3.0]), lr=0.1, max_iter=1000, tol=1e-10)
    assert res.converged
    assert res.loss < 1e-6
    np.testing.assert_allclose(res.x, np.zeros(2), atol=1e-4)


def test_nelder_mead_minimiza_cuadratica() -> None:
    def f(x: np.ndarray) -> float:
        return float(np.sum(x**2))

    res = nelder_mead(f, np.array([5.0, -3.0]), tol=1e-10)
    assert res.loss < 1e-6


def test_estimate_uncertainty() -> None:
    r = np.array([1.0, -1.0, 0.0, 2.0, -2.0])
    assert estimate_uncertainty(r) > 0
    assert estimate_uncertainty(np.array([])) == 0.0


def test_validate() -> None:
    res = OptimizationResult(x=np.zeros(2), loss=0.0, iterations=1, converged=True, history=[0.0])
    assert validate(res, max_loss=1.0) is True
    res2 = OptimizationResult(x=np.zeros(2), loss=5.0, iterations=1, converged=False, history=[5.0])
    assert validate(res2, max_loss=1.0) is False
