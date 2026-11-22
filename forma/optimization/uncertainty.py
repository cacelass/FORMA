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
    pred = np.asarray(pred, dtype=float)
    return pred - z * std, pred + z * std
