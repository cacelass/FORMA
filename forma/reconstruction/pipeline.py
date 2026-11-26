"""Pipeline de reconstrucción desde fotos."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from forma.core.anatomy import build_twin
from forma.optimization.engine import nelder_mead


@dataclass
class Landmarks:
    points: np.ndarray  # (K, 2) or (K, 3)
    confidence: np.ndarray = field(default_factory=lambda: np.ones(0))

    def __post_init__(self) -> None:
        self.points = np.asarray(self.points, dtype=float)
        if self.points.ndim != 2 or self.points.shape[1] not in (2, 3):
            raise ValueError("landmarks debe ser (K,2) o (K,3)")


@dataclass
class ReconstructionResult:
    twin: Any
    landmarks: Landmarks
    metadata: dict[str, Any] = field(default_factory=dict)
    loss: float = 0.0


class ReconstructionPipeline:
    def __init__(self) -> None:
        self.twin = build_twin()

    def preprocess(self, image: np.ndarray) -> np.ndarray:
        img = np.asarray(image, dtype=float)
        if img.ndim not in (2, 3):
            raise ValueError("imagen inválida")
        # normalización simple
        if img.size == 0:
            raise ValueError("imagen vacía")
        return (img - img.mean()) / (img.std() + 1e-8)

    def estimate_pose(self, image: np.ndarray) -> Landmarks:
        img = self.preprocess(image)
        # stub: genera landmarks sintéticos a partir del tamaño
        k = 17
        pts = np.zeros((k, 2))
        h, w = (img.shape[0], img.shape[1]) if img.ndim >= 2 else (10, 10)
        for i in range(k):
            pts[i] = (w * (i % 5) / 5.0, h * (i // 5) / 4.0)
        conf = np.ones(k)
        return Landmarks(points=pts, confidence=conf)

    def anthropometry(self, landmarks: Landmarks) -> dict[str, float]:
        pts = landmarks.points
        if pts.shape[0] < 2:
            return {}
        # altura estimada = span vertical
        ys = pts[:, 1]
        height = float(ys.max() - ys.min())
        return {"height_px": height, "landmark_count": float(pts.shape[0])}

    def multiview_fit(self, views: list[np.ndarray]) -> np.ndarray:
        if not views:
            raise ValueError("sin vistas")
        # concatena landmarks de cada vista
        all_pts = []
        for v in views:
            lm = self.estimate_pose(v)
            all_pts.append(lm.points)
        return np.concatenate(all_pts, axis=0)

    def fit(self, views: list[np.ndarray]) -> ReconstructionResult:
        if not views:
            raise ValueError("sin vistas")
        combined = self.multiview_fit(views)
        anthro = self.anthropometry(Landmarks(points=combined))
        # optimización: ajustar vector del twin a un target sintético
        bone_names = list(self.twin.skeleton.bone_lengths.keys())
        muscle_names = list(self.twin.muscles.keys())
        adipose_regions = list(self.twin.adipose.regions.keys())
        if not adipose_regions:
            adipose_regions = ["default"]
            self.twin.adipose.regions = {"default": 1.0}
        target = np.ones(len(bone_names) + len(muscle_names) + len(adipose_regions))
        x0 = self.twin.to_vector()

        def f(x: np.ndarray) -> float:
            return float(np.sum((x - target) ** 2))

        res = nelder_mead(f, x0, max_iter=200, tol=1e-6)
        from forma.core.model import DigitalTwin

        new_twin = DigitalTwin.from_vector(
            self.twin.person_id, res.x, bone_names, muscle_names, adipose_regions
        )
        meta = {"views": len(views), "anthropometry": anthro, "iterations": res.iterations}
        return ReconstructionResult(
            twin=new_twin, landmarks=Landmarks(points=combined), metadata=meta, loss=res.loss
        )

    def persist(self, result: ReconstructionResult, path: str) -> None:
        from forma.persistence.store import save_twin

        save_twin(result.twin, path)
        # metadata sidecar
        import json
        from pathlib import Path

        sidecar = Path(path).with_suffix(".meta.json")
        sidecar.write_text(json.dumps(result.metadata, indent=2), encoding="utf-8")
