"""Benchmark de optimizadores."""

from __future__ import annotations

from typing import Callable

import numpy as np

from forma.optimization.engine import OptimizationResult
from forma.optimization.engine import gradient_descent, nelder_mead
from forma.optimization.optimizers import adam, rmsprop, sgd_momentum


def benchmark(f: Callable[[np.ndarray], float], grad: Callable[[np.ndarray], np.ndarray], x0: np.ndarray) -> dict[str, OptimizationResult]:
    return {
        "gradient_descent": gradient_descent(f, grad, x0),
        "adam": adam(f, x0),
        "rmsprop": rmsprop(f, x0),
        "sgd_momentum": sgd_momentum(f, x0),
        "nelder_mead": nelder_mead(f, x0),
    }
