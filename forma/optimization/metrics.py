"""Métricas de evaluación."""

from __future__ import annotations

import numpy as np


def _check_shape(pred: np.ndarray, target: np.ndarray) -> None:
    if pred.shape != target.shape:
        raise ValueError("formas distintas")


def rmse(pred: np.ndarray, target: np.ndarray) -> float:
    pred = np.asarray(pred, dtype=float)
    target = np.asarray(target, dtype=float)
    _check_shape(pred, target)
    return float(np.sqrt(np.mean((pred - target) ** 2)))


def r2(pred: np.ndarray, target: np.ndarray) -> float:
    pred = np.asarray(pred, dtype=float)
    target = np.asarray(target, dtype=float)
    _check_shape(pred, target)
    ss_res = float(np.sum((target - pred) ** 2))
    ss_tot = float(np.sum((target - np.mean(target)) ** 2))
    if ss_tot == 0:
        return 1.0 if ss_res == 0 else 0.0
    return 1.0 - ss_res / ss_tot


def mape(pred: np.ndarray, target: np.ndarray) -> float:
    pred = np.asarray(pred, dtype=float)
    target = np.asarray(target, dtype=float)
    _check_shape(pred, target)
    denom = np.where(np.abs(target) < 1e-12, 1.0, np.abs(target))
    return float(np.mean(np.abs((target - pred) / denom)) * 100.0)


def mae(pred: np.ndarray, target: np.ndarray) -> float:
    pred = np.asarray(pred, dtype=float)
    target = np.asarray(target, dtype=float)
    _check_shape(pred, target)
    return float(np.mean(np.abs(pred - target)))
