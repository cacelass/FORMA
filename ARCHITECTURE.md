# Architecture — FORMA

See `vault/01_PROYECTO/arquitectura.md` for the full design. Summary:

## Layers
1. Skeleton — bone proportions, joints, constraints, asymmetries.
2. Muscular system — parametrized muscles (origin/insertion, volume, length, thickness).
3. Adipose tissue — regional subcutaneous fat, measured vs. estimated.
4. Skin and surface — external geometry, UV, materials, SSS.
5. External objects — clothing, tattoos, accessories (independent of anatomy).

## Components (existentes)
- Core anatomical model (`forma/core/`) — Skeleton, Muscle, AdiposeLayer, Skin, DigitalTwin
- Parametric optimization engine (`forma/optimization/`) — losses, optimizers, metrics, search, uncertainty
- Persistence and versioning (`forma/persistence/`) — serialización JSON
- Application modules (`forma/modules/`) — fitness, fashion, body_art
- Base body provider abstraction (`forma/providers/`)

## Components (previstos, bloqueados por infraestructura 3D)
- Reconstruction pipeline (`forma/reconstruction/`)
- Interaction engine (`forma/interaction/`)
- Platform interface / viewport 3D (`forma/ui/`)

## Key invariant
The anatomical core does not depend on the render engine or the UI. It is consumable as a library/service.
