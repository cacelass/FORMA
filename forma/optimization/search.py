"""Búsqueda y multi-start."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np

from forma.optimization.engine import OptimizationResult
from forma.optimization.optimizers import adam


def multi_start(
    f: Callable[[np.ndarray], float],
    x0: np.ndarray,
    n_restarts: int = 5,
    noise: float = 0.5,
    seed: int = 0,
    **kwargs: Any,
) -> OptimizationResult:
    rng = np.random.default_rng(seed)
    best: OptimizationResult | None = None
    for _ in range(n_restarts):
        cand = x0 + rng.normal(0, noise, size=x0.shape)
        res = adam(f, cand, **kwargs)
        if best is None or res.loss < best.loss:
            best = res
    if best is None:
        raise RuntimeError("multi_start no produjo resultado")
    return best


def grid_search(
    f: Callable[[np.ndarray], float],
    bounds: list[tuple[float, float]],
    steps: int = 10,
) -> OptimizationResult:
    from itertools import product

    axes = [np.linspace(lo, hi, steps) for lo, hi in bounds]
    best_x = None
    best_val = float("inf")
    for combo in product(*axes):
        x = np.asarray(combo, dtype=float)
        v = f(x)
        if v < best_val:
            best_val = v
            best_x = x
    if best_x is None:
        raise RuntimeError("grid_search no produjo resultado")
    return OptimizationResult(
        x=best_x, loss=best_val, iterations=steps ** len(bounds), converged=True, history=[best_val]
    )
