# Implementation Plan — FORMA

## Phase 0 — Technical Research (done)
Audit base meshes, licensing, Blender/ML architecture, data model, MVP plan. Deliverables: ARCHITECTURE.md, TECHNICAL_DECISIONS.md, IMPLEMENTATION_PLAN.md.

## Phase 1 — 3D Foundation (bloqueada: requiere Blender)
BlenderBridge, load base human model, render views, save/reload. Depends on BASE-001.

## Phase 2 — Parametric Anatomy
Skeletal params, muscle registry, localized deformation, constraints, independence validation.

## Phase 3 — Photo Reconstruction (bloqueada)
Preprocessing, pose, landmarks, anthropometry, multiview fitting, optimization, metadata.

## Phase 4 — Surface and Skin (bloqueada)
Surface geometry, UV, skin materials, realistic rendering, texture deformation.

## Phase 5 — General Interaction Engine (bloqueada)
Surface attachment, object positioning, collision, deformation tracking, simulation interfaces.

## Phase 6 — Application Modules
Fitness, fashion, body art, ergonomics, aesthetics, animation, education modules (>=3).

## Phase 7 — Platform Interface (bloqueada)
3D viewport, parameter editing, config management, reconstruction interface, export/comparison.

## MVP-001
3 photos → persistent 3D digital twin with editable muscles (deltoid/pectoral/biceps/abdomen), save/compare configs.

## Cross-cutting
- BASE-001: evaluate base human body providers (done).
- OPT-001: optimization engine for reconstruction (bloqueada).
- OPT-002: motor de optimización puro Python (done).
- IMPROVE-001: mejoras ML y persistencia (done).
