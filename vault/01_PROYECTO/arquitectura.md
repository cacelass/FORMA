# Arquitectura — FORMA

## Piezas del sistema (existentes)

1. **Núcleo anatómico** (`forma/core/`): modelo paramétrico con capas independientes:
   - Esqueleto: proporciones óseas, articulaciones, restricciones, asimetrías.
   - Sistema muscular: músculos parametrizados (origen/inserción, volumen, longitud, grosor).
   - Tejido adiposo: grasa subcutánea regional, separando medido de estimado.
   - Piel y superficie: geometría externa, UV, materiales, SSS.
2. **Motor de optimización** (`forma/optimization/`): losses, optimizadores (GD, Adam, RMSprop, SGD), métricas, búsqueda multi-start/grid, incertidumbre (bootstrap).
3. **Persistencia y versionado** (`forma/persistence/`): serialización JSON del gemelo.
4. **Módulos de aplicación** (`forma/modules/`): fitness, fashion, body art.
5. **Abstracción de proveedor base** (`forma/providers/`): `BaseBodyProvider`.

## Piezas previstas (bloqueadas por infraestructura 3D)

6. **Pipeline de reconstrucción** (`forma/reconstruction/`): fotos → pose/landmarks → antropometría → fitting multivista → optimización → gemelo persistente.
7. **Motor de interacción** (`forma/interaction/`): attachment a superficie, posicionamiento de objetos, colisión, tracking.
8. **Interfaz de plataforma** (`forma/ui/`): viewport 3D, edición de parámetros, gestión de configuraciones, exportación.

## Flujo

```
fotos (3 vistas) → preprocessing → pose/landmarks → antropometría
  → fitting multivista → optimización → gemelo persistente (capas)
  → edición paramétrica por capa → guardar/comparar configuraciones
  → exportación / consumo por módulos de aplicación
```

El núcleo anatómico no depende del motor de render ni de la interfaz.

## Stack

- Lenguaje: Python 3.12+ (el `.venv` de referencia es 3.13).
- Entorno y dependencias: uv (`uv.lock`).
- Calidad: ruff, mypy, pytest, bandit, pip-audit.
- Conocimiento: vault Obsidian + graphify + RAG local opcional (chromadb).
- 3D: proveedor base elegido en BASE-001 (recomendación en proveedores-cuerpo-base.md); implementación en PHASE-1 (bloqueada).

## Alternativas consideradas y descartadas

- **Monolito por aplicación** (un módulo por caso de uso, con su propia geometría): descartado porque duplica el modelo anatómico y rompe la reutilización del gemelo entre aplicaciones; el principio central es "una persona, un gemelo persistente, múltiples aplicaciones".
- **Depender del motor de render para el núcleo**: descartado para que el gemelo sea consumible como biblioteca/servicio sin GPU ni UI.

## Riesgos conocidos

- Fitting multivista desde 3 fotos puede ser subdeterminado; se estima incertidumbre por parámetro (OPT-001).
- Elección del proveedor base de cuerpo humano (BASE-001) bloquea PHASE-1..7; se deja para después de PHASE-0.
- Blender como dependencia pesada: a encapsular tras `BaseBodyProvider` para poder sustituirlo.

## Decisiones diferidas

- Proveedor base de cuerpo humano (BASE-001).
- Formato de persistencia del gemelo (pickle vs. glTF vs. formato propio).
- Motor de render final (Blender headless vs. trimesh/pyrender).

## Estructura del repositorio

```
forma/                 — El código del proyecto (project_slug en project.yml)
tests/                 — Tests del proyecto

agents/                — Sistema multi-agente del arnés (stdlib pura)
├── contracts.py       — Contratos de rol: can / cannot / needs / owns
├── agents/            — Un módulo por agente
├── tools/             — Herramientas compartidas
├── prompts/           — Skills cargables por el asistente
├── evals/             — Ruteo, contratos y RAG, medidos
└── workspace/         — Lo que generan los agentes (git-ignored)

harness/               — El arnés: backlog, progreso, memoria
vault/                 — Conocimiento estable (Obsidian)
docs/                  — Sphinx
```

## Las dos fronteras de seguridad

```
Agentes Python:  run() → agents/permissions.py → acción          (siempre activa)
Asistente:       herramienta → agents/policy_guard.py → Bash/... (opcional, sin cablear)
```
