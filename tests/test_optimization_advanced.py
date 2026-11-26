"""Optimizadores avanzados y métricas (mejora ML)."""

from __future__ import annotations

import numpy as np
import pytest

from forma.optimization.engine import gradient_descent, nelder_mead
from forma.optimization.losses import cosine_distance, huber, mae, mse
from forma.optimization.metrics import mape, r2, rmse
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


def test_mape() -> None:
    p = np.array([1.0, 2.0, 3.0])
    t = np.array([1.0, 2.0, 3.0])
    assert mape(p, t) == pytest.approx(0.0)


def test_cosine_distance() -> None:
    from forma.optimization.losses import cosine_distance

    a = np.array([1.0, 0.0])
    assert cosine_distance(a, a) == pytest.approx(0.0)


def test_bootstrap_ci_empty() -> None:
    from forma.optimization.uncertainty import bootstrap_ci

    assert bootstrap_ci(np.array([])) == (0.0, 0.0, 0.0)


def test_losses_formas_distintas() -> None:
    a = np.array([1.0])
    b = np.array([1.0, 2.0])
    with pytest.raises(ValueError):
        mse(a, b)
    with pytest.raises(ValueError):
        mae(a, b)
    with pytest.raises(ValueError):
        huber(a, b)


def test_cosine_distance_cero() -> None:
    from forma.optimization.losses import cosine_distance

    assert cosine_distance(np.array([0.0, 0.0]), np.array([1.0, 0.0])) == 1.0


def test_metrics_validan_forma() -> None:
    a = np.array([1.0])
    b = np.array([1.0, 2.0])
    with pytest.raises(ValueError):
        rmse(a, b)
    with pytest.raises(ValueError):
        r2(a, b)
    with pytest.raises(ValueError):
        mape(a, b)
    with pytest.raises(ValueError):
        mae(a, b)


def test_losses_validaciones() -> None:
    with pytest.raises(ValueError):
        huber(np.array([1.0]), np.array([1.0]), delta=-1.0)
    with pytest.raises(ValueError):
        cosine_distance(np.array([1.0]), np.array([1.0, 2.0]))


def test_optimizers_validaciones() -> None:
    with pytest.raises(ValueError):
        finite_difference_grad(lambda x: float(x[0]), np.array([1.0]), eps=0.0)
    with pytest.raises(ValueError):
        adam(lambda x: float(np.sum(x**2)), np.array([1.0]), beta1=1.0)
    with pytest.raises(ValueError):
        rmsprop(lambda x: float(np.sum(x**2)), np.array([1.0]), rho=1.0)
    with pytest.raises(ValueError):
        adam(lambda x: float(np.sum(x**2)), np.array([1.0]), max_iter=0)
    with pytest.raises(ValueError):
        gradient_descent(lambda x: float(np.sum(x**2)), lambda x: 2 * x, np.array([1.0]), lr=0.0)
    with pytest.raises(ValueError):
        nelder_mead(lambda x: float(np.sum(x**2)), np.array([]))


def test_uncertainty_validaciones() -> None:
    with pytest.raises(ValueError):
        bootstrap_ci(np.array([1.0]), n_boot=0)
    with pytest.raises(ValueError):
        bootstrap_ci(np.array([1.0]), ci=1.5)
    with pytest.raises(ValueError):
        prediction_interval(np.array([0.0]), -1.0)


def test_search_validaciones() -> None:
    with pytest.raises(ValueError):
        grid_search(lambda x: float(np.sum(x**2)), [])
    with pytest.raises(ValueError):
        multi_start(lambda x: float(np.sum(x**2)), np.array([1.0]), n_restarts=0)


def test_r2_constante() -> None:
    p = np.array([1.0, 1.0])
    t = np.array([2.0, 2.0])
    assert r2(p, t) == 0.0


def test_shrink_helper() -> None:
    import numpy as np

    from forma.optimization.engine import _shrink

    simplex = [np.array([0.0, 0.0]), np.array([1.0, 0.0]), np.array([0.0, 1.0])]
    fvals = [0.0, 1.0, 1.0]
    new_s, new_f = _shrink(simplex, fvals, 0, 0.5, lambda x: float(np.sum(x**2)))
    assert len(new_s) == 3
    assert new_f[0] == 0.0
