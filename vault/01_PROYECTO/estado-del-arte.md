# Estado del arte — FORMA

## Fuentes indexadas (RAG)

1. **Recovering 3D Human Mesh from Monocular Images: A Survey** (arXiv 2203.01923)
   - Qué se toma: taxonomía de paradigmas (optimización vs. regresión), body models, datasets y métricas de evaluación. Base para PHASE-3 (reconstrucción) y OPT-001.
   - Qué se descarta: los métodos asumen SMPL/SMPL-X como representación final; FORMA necesita capas independientes, así que el body model se encapsula tras `BaseBodyProvider`.

2. **SAM 3D Body: Robust Full-Body Human Mesh Recovery** (arXiv 2602.15989)
   - Qué se toma: idea de decoupling esqueleto/superficie (Momentum Human Rig) y uso de prompts 2D. Inspiración directa para la independencia de capas de FORMA.
   - Qué se descarta: dependencia de un modelo denso de keypoints; FORMA debe funcionar con 3 fotos, no con video.

3. **Motion-X / Motion-X++** (arXiv 2307.00818, 2501.05098)
   - Qué se toma: representación SMPL-X y anotación multimodal como referencia de formato de salida y de pose.
   - Qué se descarta: Motion-X es un dataset, no una plataforma; FORMA no reproduce datasets, los consume opcionalmente para validación.

## Huecos de capacidad (bootstrap suggest_agents)

Los términos no cubiertos son léxicos (adiposo, esqueleto, músculos, piel, ...), no capacidades del arnés. No se crean agentes para ellos: el arnés ya cubre desarrollo, tests, docs, git, CI, etc. Los agentes de dominio 3D (reconstrucción, fitting) se crearán con `installer scaffold` cuando se abran PHASE-1..3.

## Decisiones diferidas

- Proveedor base de cuerpo humano (BASE-001): SMPL-X vs. MakeHuman vs. MB-Lab vs. Blender-native.
- Formato de persistencia del gemelo.
