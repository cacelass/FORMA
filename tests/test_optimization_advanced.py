"""Optimizadores avanzados y métricas (mejora ML)."""

from __future__ import annotations

import numpy as np
import pytest

from forma.optimization.losses import huber, mse
from forma.optimization.metrics import mae, r2, rmse
from forma.optimization.optimizers import adam, finite_difference_grad, rmsprop, sgd_momentum
from forma.optimization.search import grid_search, multi_start
from forma.optimization.uncertainty import bootstrap_ci, prediction_interval


def _f(x: np.ndarray) -> float:
    return float(np.sum(x**2))


def test_finite_difference_grad() -> None:
    g = finite_difference_grad(_f, np.array([2.0, -1.0]))
    np.testing.assert_allclose(g, [4.0, -2.0], atol=1e-4)


def test_adam_converge() -> None:
    res = adam(_f, np.array([5.0, -3.0]), lr=0.1, max_iter=2000, tol=1e-12)
    assert res.loss < 1e-4


def test_rmsprop_converge() -> None:
    res = rmsprop(_f, np.array([5.0, -3.0]), lr=0.1, max_iter=2000, tol=1e-12)
    assert res.loss < 1e-3


def test_sgd_momentum_converge() -> None:
    res = sgd_momentum(_f, np.array([5.0, -3.0]), lr=0.01, max_iter=5000, tol=1e-12)
    assert res.loss < 1e-2


def test_multi_start() -> None:
    res = multi_start(_f, np.array([5.0, -3.0]), n_restarts=3, max_iter=2000, tol=1e-10, lr=0.1)
    assert res.loss < 1e-3


def test_grid_search() -> None:
    res = grid_search(_f, [(-5.0, 5.0), (-5.0, 5.0)], steps=11)
    assert res.loss < 0.5


def test_losses() -> None:
    a = np.array([1.0, 2.0])
    b = np.array([1.0, 2.0])
    assert mse(a, b) == 0.0
    assert huber(a, b) == 0.0


def test_metrics() -> None:
    p = np.array([1.0, 2.0, 3.0])
    t = np.array([1.0, 2.0, 3.0])
    assert rmse(p, t) == 0.0
    assert r2(p, t) == pytest.approx(1.0)
    assert mae(p, t) == 0.0


def test_bootstrap_ci() -> None:
    r = np.array([1.0, -1.0, 0.5, -0.5, 2.0, -2.0])
    mean, lo, hi = bootstrap_ci(r, n_boot=200)
    assert lo <= mean <= hi


def test_prediction_interval() -> None:
    pred = np.array([0.0, 1.0])
    lo, hi = prediction_interval(pred, 1.0)
    assert (hi > lo).all()
