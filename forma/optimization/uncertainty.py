"""Incertidumbre: bootstrap y intervalos de confianza."""

from __future__ import annotations

import numpy as np


def bootstrap_ci(
    residuals: np.ndarray,
    n_boot: int = 1000,
    ci: float = 0.95,
    seed: int = 0,
) -> tuple[float, float, float]:
    """Devuelve (media, lower, upper) del bootstrap de los residuos."""
    if n_boot < 1:
        raise ValueError("n_boot debe ser >= 1")
    if not (0 < ci < 1):
        raise ValueError("ci debe estar en (0,1)")
    r = np.asarray(residuals, dtype=float).ravel()
    if r.size == 0:
        return 0.0, 0.0, 0.0
    rng = np.random.default_rng(seed)
    means = np.array(
        [float(np.mean(rng.choice(r, size=r.size, replace=True))) for _ in range(n_boot)]
    )
    alpha = (1 - ci) / 2
    lower = float(np.quantile(means, alpha))
    upper = float(np.quantile(means, 1 - alpha))
    return float(np.mean(r)), lower, upper


def prediction_interval(
    pred: np.ndarray, std: float, z: float = 1.96
) -> tuple[np.ndarray, np.ndarray]:
    if std < 0:
        raise ValueError("std debe ser >= 0")
    pred = np.asarray(pred, dtype=float)
    return pred - z * std, pred + z * std
