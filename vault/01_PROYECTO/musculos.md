# Modelado muscular individual — FORMA

## Principio

El gemelo digital es un ABM (anatomy-based model): cada músculo se modela
individualmente con su origen, inserción, forma, volumen y comportamiento
(fuerza-longitud, fuerza-velocidad). El comportamiento individual es necesario
para simular contracción, fuerza y movimiento.

## Capas (orden de construcción)

1. **Estructura ósea** (`forma/core/anatomy.py` → `build_skeleton`): landmarks y longitudes.
2. **Músculos** (`MUSCLE_CATALOG`): origen, inserción, función, volumen, dirección de fibra, agonistas/antagonistas.
3. **Comportamiento** (`forma/core/muscle_behavior.py`): modelo de Hill (fuerza-longitud, fuerza-velocidad, fuerza isométrica/dinámica).
4. **Grasa** (`AdiposeLayer`): regional, medido vs estimado.
5. **Piel/superficie** (`forma/surface/`): malla, UV, material.

## Músculos modelados (catálogo)

| Músculo | Origen | Inserción | Función | Volumen | Fibras |
|---------|--------|-----------|---------|---------|--------|
| deltoides | shoulder_r | elbow_r | abducción hombro | 0.4 | multipennate |
| pectoral_mayor | shoulder_r | thoracic | aducción/flexión hombro | 0.6 | fan |
| biceps_braquial | shoulder_r | elbow_r | flexión codo | 0.25 | fusiforme |
| triceps_braquial | shoulder_r | elbow_r | extensión codo | 0.35 | pennate |
| recto_abdominal | pelvis | thoracic | flexión tronco | 0.3 | strap |
| cuadriceps | hip_r | knee_r | extensión rodilla | 0.8 | pennate |
| isquiotibiales | pelvis | knee_r | flexión rodilla | 0.5 | bipennate |
| gastrocnemio | knee_r | ankle_r | flexión plantar | 0.3 | pennate |
| dorsal_ancho | thoracic | shoulder_r | extensión hombro | 0.7 | fan |
| trapecio | cervical | shoulder_r | elevación escapular | 0.4 | triangular |

## Papers indexados (RAG)

- "A three-dimensional model of skeletal muscle tissues" (arXiv 2207.02421)
- "On the dynamical stability of skeletal muscle" (arXiv 2601.05275)
- "Muscle Excitation Estimation in Biomechanical Simulation" (arXiv 1809.06121)

## ABM

`forma/abm/engine.py` → `AnatomyBasedModel`: activación individual, fuerza total, balance agonista/antagonista.
