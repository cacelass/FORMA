"""Motor de optimización para reconstrucción (OPT-001/OPT-002)."""

from forma.optimization.engine import (
    OptimizationResult,
    estimate_uncertainty,
    gradient_descent,
    l2_loss,
    nelder_mead,
    validate,
)
from forma.optimization.losses import cosine_distance, huber, mae, mse
from forma.optimization.metrics import mae as metric_mae
from forma.optimization.metrics import mape, r2, rmse
from forma.optimization.optimizers import adam, finite_difference_grad, rmsprop, sgd_momentum
from forma.optimization.search import grid_search, multi_start
from forma.optimization.uncertainty import bootstrap_ci, prediction_interval

__all__ = [
    "OptimizationResult",
    "estimate_uncertainty",
    "gradient_descent",
    "l2_loss",
    "nelder_mead",
    "validate",
    "cosine_distance",
    "huber",
    "mse",
    "mae",
    "rmse",
    "metric_mae",
    "r2",
    "mape",
    "adam",
    "finite_difference_grad",
    "rmsprop",
    "sgd_momentum",
    "multi_start",
    "grid_search",
    "bootstrap_ci",
    "prediction_interval",
]
