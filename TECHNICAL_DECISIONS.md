# Technical Decisions — FORMA

## TD-001: Layered parametric model
Decision: independent, replaceable layers (skeleton → muscle → adipose → skin).
Reason: allows per-component modification without breaking coherence of the rest.

## TD-002: Python 3.12+ with uv
Decision: stdlib-first arnés, uv for deps.
Reason: reproducible, no heavy framework.

## TD-003: BaseBodyProvider abstraction (deferred)
Decision: encapsulate the body provider behind an interface; concrete provider chosen in BASE-001.
Reason: allows swapping SMPL-X / MakeHuman / MB-Lab / Blender-native without touching the core.

## TD-004: Persistence format (parcial)
Decision: JSON para el gemelo (forma/persistence/store.py, IMPROVE-001). glTF/pickle quedan diferidos a MVP-001 para exportación 3D.

## TD-006: Motor de optimización puro Python
Decision: implementar el motor de optimización sin dependencias externas (numpy solo), con optimizadores adaptativos (Adam, RMSprop, SGD), métricas y bootstrap. Rastreado en OPT-002/IMPROVE-001.

## TD-005: Render engine (deferred)
Decision: to be decided (Blender headless vs. trimesh/pyrender). Tracked in PHASE-4.
