"""Motor de optimización: minimiza la diferencia entre el gemelo y la evidencia."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np


@dataclass
class OptimizationResult:
    x: np.ndarray
    loss: float
    iterations: int
    converged: bool
    history: list[float]


def l2_loss(pred: np.ndarray, target: np.ndarray) -> float:
    if pred.shape != target.shape:
        raise ValueError("formas distintas")
    return float(np.sqrt(np.mean((pred - target) ** 2)))


def gradient_descent(
    f: Callable[[np.ndarray], float],
    grad: Callable[[np.ndarray], np.ndarray],
    x0: np.ndarray,
    lr: float = 1e-2,
    max_iter: int = 1000,
    tol: float = 1e-8,
) -> OptimizationResult:
    x = np.asarray(x0, dtype=float).copy()
    history: list[float] = []
    converged = False
    for i in range(max_iter):
        g = grad(x)
        x = x - lr * g
        val = f(x)
        history.append(val)
        if i > 0 and abs(history[-2] - history[-1]) < tol:
            converged = True
            break
    return OptimizationResult(
        x=x, loss=float(f(x)), iterations=len(history), converged=converged, history=history
    )


def nelder_mead(
    f: Callable[[np.ndarray], float],
    x0: np.ndarray,
    max_iter: int = 2000,
    alpha: float = 1.0,
    gamma: float = 2.0,
    rho: float = 0.5,
    sigma: float = 0.5,
    tol: float = 1e-8,
) -> OptimizationResult:
    n = len(x0)
    simplex = [np.asarray(x0, dtype=float).copy()]
    for i in range(n):
        y = x0.copy()
        y[i] = y[i] * 1.05 if y[i] != 0 else 0.01
        simplex.append(y)
    fvals = [f(p) for p in simplex]
    history: list[float] = [min(fvals)]
    converged = False
    for _ in range(max_iter):
        order = sorted(range(len(simplex)), key=lambda i: fvals[i])
        best = order[0]
        worst = order[-1]
        second = order[-2]
        centroid = np.mean([simplex[i] for i in order[:-1]], axis=0)
        xr = centroid + alpha * (centroid - simplex[worst])
        fr = f(xr)
        if fr < fvals[best]:
            xe = centroid + gamma * (centroid - simplex[worst])
            fe = f(xe)
            if fe < fr:
                simplex[worst] = xe
                fvals[worst] = fe
            else:
                simplex[worst] = xr
                fvals[worst] = fr
        elif fr < fvals[second]:
            simplex[worst] = xr
            fvals[worst] = fr
        else:
            xc = centroid + rho * (simplex[worst] - centroid)
            fc = f(xc)
            if fc < fvals[worst]:
                simplex[worst] = xc
                fvals[worst] = fc
            else:
                for i in range(len(simplex)):
                    if i == best:
                        continue
                    simplex[i] = simplex[best] + sigma * (simplex[i] - simplex[best])
                    fvals[i] = f(simplex[i])
        history.append(min(fvals))
        spread = max(fvals) - min(fvals)
        if spread < tol:
            converged = True
            break
    bi = int(np.argmin(fvals))
    return OptimizationResult(
        x=simplex[bi],
        loss=float(fvals[bi]),
        iterations=len(history),
        converged=converged,
        history=history,
    )


def estimate_uncertainty(residuals: np.ndarray) -> float:
    """Incertidumbre = desviación estándar de los residuos."""
    r = np.asarray(residuals, dtype=float).ravel()
    if r.size == 0:
        return 0.0
    return float(np.std(r))


def validate(result: OptimizationResult, max_loss: float) -> bool:
    return bool(result.converged or result.loss <= max_loss)
