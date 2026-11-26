"""Serialización JSON del DigitalTwin."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from forma.core.model import AdiposeLayer, DigitalTwin, Muscle, Skeleton


def _to_dict(twin: DigitalTwin) -> dict[str, Any]:
    return {
        "person_id": twin.person_id,
        "skeleton": {
            "bone_lengths": twin.skeleton.bone_lengths,
            "joints": {k: list(v) for k, v in twin.skeleton.joints.items()},
        },
        "muscles": {
            k: {
                "name": m.name,
                "origin": m.origin,
                "insertion": m.insertion,
                "volume": m.volume,
                "length": m.length,
                "thickness": m.thickness,
            }
            for k, m in twin.muscles.items()
        },
        "adipose": {"regions": twin.adipose.regions},
        "skin": {
            "vertex_count": twin.skin.vertex_count,
            "uv": twin.skin.uv,
            "material": twin.skin.material,
        },
        "metadata": twin.metadata,
    }


def save_twin(twin: DigitalTwin, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_to_dict(twin), indent=2, ensure_ascii=False), encoding="utf-8")


def load_twin(path: str | Path) -> DigitalTwin:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("JSON inválido: se esperaba un objeto")
    if not isinstance(data.get("person_id"), str) or not data["person_id"]:
        raise ValueError("person_id debe ser string no vacío")
    sk_data = data.get("skeleton")
    if not isinstance(sk_data, dict):
        raise ValueError("skeleton inválido")
    joints_raw = sk_data.get("joints", {})
    if not isinstance(joints_raw, dict):
        raise ValueError("joints inválido")
    for k, v in joints_raw.items():
        if not (isinstance(v, (list, tuple)) and len(v) == 3):
            raise ValueError(f"joint '{k}' debe tener 3 coordenadas")
    meta = data.get("metadata", {})
    if not isinstance(meta, dict):
        raise ValueError("metadata inválido")
    sk = Skeleton(
        bone_lengths=sk_data.get("bone_lengths", {}),
        joints={k: tuple(v) for k, v in joints_raw.items()},
    )
    muscles = {k: Muscle(**v) for k, v in data["muscles"].items()}
    adipose = AdiposeLayer(regions=data["adipose"]["regions"])
    from forma.core.model import Skin

    skin = Skin(**data["skin"])
    return DigitalTwin(
        person_id=data["person_id"],
        skeleton=sk,
        muscles=muscles,
        adipose=adipose,
        skin=skin,
        metadata=data.get("metadata", {}),
    )
