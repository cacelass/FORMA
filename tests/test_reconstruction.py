"""Pipeline de reconstrucción (PHASE-3)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from forma.reconstruction.pipeline import Landmarks, ReconstructionPipeline, ReconstructionResult


def test_preprocess() -> None:
    p = ReconstructionPipeline()
    img = np.arange(12, dtype=float).reshape(3, 4)
    out = p.preprocess(img)
    assert out.shape == img.shape


def test_estimate_pose() -> None:
    p = ReconstructionPipeline()
    img = np.zeros((10, 10))
    lm = p.estimate_pose(img)
    assert lm.points.shape[1] == 2
    assert lm.points.shape[0] == 17


def test_anthropometry() -> None:
    p = ReconstructionPipeline()
    lm = Landmarks(points=np.array([[0, 0], [0, 10]]))
    a = p.anthropometry(lm)
    assert a["height_px"] == 10.0


def test_multiview_fit() -> None:
    p = ReconstructionPipeline()
    views = [np.zeros((10, 10)), np.zeros((10, 10))]
    combined = p.multiview_fit(views)
    assert combined.shape[0] == 34


def test_fit() -> None:
    p = ReconstructionPipeline()
    views = [np.zeros((10, 10))]
    res = p.fit(views)
    assert isinstance(res, ReconstructionResult)
    assert res.loss >= 0
    assert "views" in res.metadata


def test_fit_sin_vistas() -> None:
    p = ReconstructionPipeline()
    with pytest.raises(ValueError):
        p.fit([])


def test_landmarks_validacion() -> None:
    with pytest.raises(ValueError):
        Landmarks(points=np.array([1.0, 2.0]))


def test_persist(tmp_path: Path) -> None:
    p = ReconstructionPipeline()
    res = p.fit([np.zeros((10, 10))])
    out = tmp_path / "twin.json"
    p.persist(res, str(out))
    assert out.exists()
    assert out.with_suffix(".meta.json").exists()
