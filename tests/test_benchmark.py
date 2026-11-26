"""Benchmark de optimizadores (OPT-001)."""

from __future__ import annotations

import numpy as np

from forma.optimization.benchmark import benchmark


def test_benchmark() -> None:
    def f(x: np.ndarray) -> float:
        return float(np.sum(x**2))

    def g(x: np.ndarray) -> np.ndarray:
        return 2 * x

    res = benchmark(f, g, np.array([3.0, -2.0]))
    assert "adam" in res
    assert "nelder_mead" in res
    assert res["adam"].loss < 1.0
