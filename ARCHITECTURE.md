# Architecture — FORMA

See `vault/01_PROYECTO/arquitectura.md` for the full design. Summary:

## Layers
1. Skeleton — bone proportions, joints, constraints, asymmetries.
2. Muscular system — parametrized muscles (origin/insertion, volume, length, thickness).
3. Adipose tissue — regional subcutaneous fat, measured vs. estimated.
4. Skin and surface — external geometry, UV, materials, SSS.
5. External objects — clothing, tattoos, accessories (independent of anatomy).

## Components
- Core anatomical model (`forma/core/`)
- Reconstruction pipeline (`forma/reconstruction/`)
- Interaction engine (`forma/interaction/`)
- Persistence and versioning (`forma/persistence/`)
- Application modules (`forma/modules/`)
- Platform interface (`forma/ui/`)

## Key invariant
The anatomical core does not depend on the render engine or the UI. It is consumable as a library/service.
