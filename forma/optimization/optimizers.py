"""Optimizadores adaptativos y de primer orden."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

from forma.optimization.engine import OptimizationResult


def finite_difference_grad(
    f: Callable[[np.ndarray], float], x: np.ndarray, eps: float = 1e-5
) -> np.ndarray:
    if eps <= 0:
        raise ValueError("eps debe ser > 0")
    x = np.atleast_1d(np.asarray(x, dtype=float))
    if x.ndim != 1:
        raise ValueError("x debe ser 1-D")
    g = np.zeros_like(x)
    for i in range(x.size):
        xp = x.copy()
        xm = x.copy()
        xp[i] += eps
        xm[i] -= eps
        g[i] = (f(xp) - f(xm)) / (2 * eps)
    return g


def adam(
    f: Callable[[np.ndarray], float],
    x0: np.ndarray,
    lr: float = 1e-2,
    beta1: float = 0.9,
    beta2: float = 0.999,
    eps: float = 1e-8,
    max_iter: int = 1000,
    tol: float = 1e-8,
    grad: Callable[[np.ndarray], np.ndarray] | None = None,
) -> OptimizationResult:
    if lr <= 0:
        raise ValueError("lr debe ser > 0")
    if not (0 <= beta1 < 1):
        raise ValueError("beta1 debe estar en [0,1)")
    if not (0 <= beta2 < 1):
        raise ValueError("beta2 debe estar en [0,1)")
    if eps <= 0:
        raise ValueError("eps debe ser > 0")
    if max_iter < 1:
        raise ValueError("max_iter debe ser >= 1")
    x = np.atleast_1d(np.asarray(x0, dtype=float)).copy()
    m = np.zeros_like(x)
    v = np.zeros_like(x)
    history: list[float] = []
    converged = False
    for i in range(1, max_iter + 1):
        g = grad(x) if grad is not None else finite_difference_grad(f, x)
        m = beta1 * m + (1 - beta1) * g
        v = beta2 * v + (1 - beta2) * (g * g)
        mhat = m / (1 - beta1**i)
        vhat = v / (1 - beta2**i)
        x = x - lr * mhat / (np.sqrt(vhat) + eps)
        val = f(x)
        history.append(val)
        if i > 1 and abs(history[-2] - history[-1]) < tol:
            converged = True
            break
    return OptimizationResult(
        x=x, loss=float(f(x)), iterations=len(history), converged=converged, history=history
    )


def rmsprop(
    f: Callable[[np.ndarray], float],
    x0: np.ndarray,
    lr: float = 1e-2,
    rho: float = 0.9,
    eps: float = 1e-8,
    max_iter: int = 1000,
    tol: float = 1e-8,
    grad: Callable[[np.ndarray], np.ndarray] | None = None,
) -> OptimizationResult:
    if lr <= 0:
        raise ValueError("lr debe ser > 0")
    if not (0 <= rho < 1):
        raise ValueError("rho debe estar en [0,1)")
    if eps <= 0:
        raise ValueError("eps debe ser > 0")
    if max_iter < 1:
        raise ValueError("max_iter debe ser >= 1")
    x = np.atleast_1d(np.asarray(x0, dtype=float)).copy()
    v = np.zeros_like(x)
    history: list[float] = []
    converged = False
    for i in range(max_iter):
        g = grad(x) if grad is not None else finite_difference_grad(f, x)
        v = rho * v + (1 - rho) * (g * g)
        x = x - lr * g / (np.sqrt(v) + eps)
        val = f(x)
        history.append(val)
        if i > 0 and abs(history[-2] - history[-1]) < tol:
            converged = True
            break
    return OptimizationResult(
        x=x, loss=float(f(x)), iterations=len(history), converged=converged, history=history
    )


def sgd_momentum(
    f: Callable[[np.ndarray], float],
    x0: np.ndarray,
    lr: float = 1e-2,
    momentum: float = 0.9,
    max_iter: int = 1000,
    tol: float = 1e-8,
    grad: Callable[[np.ndarray], np.ndarray] | None = None,
) -> OptimizationResult:
    if lr <= 0:
        raise ValueError("lr debe ser > 0")
    if max_iter < 1:
        raise ValueError("max_iter debe ser >= 1")
    x = np.atleast_1d(np.asarray(x0, dtype=float)).copy()
    velocity = np.zeros_like(x)
    history: list[float] = []
    converged = False
    for i in range(max_iter):
        g = grad(x) if grad is not None else finite_difference_grad(f, x)
        velocity = momentum * velocity - lr * g
        x = x + velocity
        val = f(x)
        history.append(val)
        if i > 0 and abs(history[-2] - history[-1]) < tol:
            converged = True
            break
    return OptimizationResult(
        x=x, loss=float(f(x)), iterations=len(history), converged=converged, history=history
    )
