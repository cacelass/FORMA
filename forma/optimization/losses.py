"""Funciones de pérdida adicionales."""

from __future__ import annotations

import numpy as np


def mse(pred: np.ndarray, target: np.ndarray) -> float:
    pred = np.asarray(pred, dtype=float)
    target = np.asarray(target, dtype=float)
    if pred.shape != target.shape:
        raise ValueError("formas distintas")
    return float(np.mean((pred - target) ** 2))


def mae(pred: np.ndarray, target: np.ndarray) -> float:
    pred = np.asarray(pred, dtype=float)
    target = np.asarray(target, dtype=float)
    if pred.shape != target.shape:
        raise ValueError("formas distintas")
    return float(np.mean(np.abs(pred - target)))


def huber(pred: np.ndarray, target: np.ndarray, delta: float = 1.0) -> float:
    pred = np.asarray(pred, dtype=float)
    target = np.asarray(target, dtype=float)
    if pred.shape != target.shape:
        raise ValueError("formas distintas")
    r = pred - target
    absr = np.abs(r)
    quad = np.minimum(absr, delta)
    lin = absr - quad
    return float(np.mean(0.5 * quad**2 + delta * lin))


def cosine_distance(pred: np.ndarray, target: np.ndarray) -> float:
    pred = np.asarray(pred, dtype=float).ravel()
    target = np.asarray(target, dtype=float).ravel()
    denom = np.linalg.norm(pred) * np.linalg.norm(target)
    if denom == 0:
        return 1.0
    return float(1.0 - np.dot(pred, target) / denom)
