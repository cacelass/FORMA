# Changelog

Todos los cambios relevantes del proyecto se documentan aquí.
Formato basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/).

El dueño de este fichero es el agente `documentation`: `git commit_feature`
añade aquí una entrada por cada feature cerrada del arnés.

---

## [Unreleased] — 2026-11-26

### Añadido

- Pulir musculos al maximo: modelo enriquecido (IMPROVE-007)

## [Unreleased] — 2026-11-26

### Añadido

- MVP: personalized 3D digital twin from 3 photos (MVP-001)

## [Unreleased] — 2026-11-26

### Añadido

- Optimization engine for reconstruction (OPT-001)

## [Unreleased] — 2026-11-26

### Añadido

- Phase 3: Photo Reconstruction (PHASE-3)

## [Unreleased] — 2026-11-26

### Añadido

- Modelado anatomico individual: musculos y ABM (IMPROVE-006)

## [Unreleased] — 2026-11-26

### Añadido

- Phase 7: Platform Interface (PHASE-7)

## [Unreleased] — 2026-11-26

### Añadido

- Phase 5: General Interaction Engine (PHASE-5)

## [Unreleased] — 2026-11-26

### Añadido

- Phase 4: Surface and Skin (PHASE-4)

## [Unreleased] — 2026-11-26

### Añadido

- Validaciones y robustez del motor ML (IMPROVE-005)

## [Unreleased] — 2026-11-26

### Añadido

- Agentes de dominio scaffold + cobertura (IMPROVE-004)

## [Unreleased] — 2026-11-26

### Añadido

- Limpieza: codigo muerto y tests faltantes (IMPROVE-003)

## [Unreleased] — 2026-11-26

### Añadido

- Alinear documentacion con estado real (IMPROVE-002)

## [Unreleased] — 2026-11-26

### Añadido

- Sincronizar arnes con MeshHarmes upstream (HARNESS-SYNC-001)

## [Unreleased] — 2026-11-22

### Añadido

- Mejoras ML: optimizadores, metricas, persistencia (IMPROVE-001)

## [Unreleased] — 2026-11-22

### Añadido

- Phase 6: Application Modules (PHASE-6)

## [Unreleased] — 2026-11-22

### Añadido

- Phase 2: Parametric Anatomy (PHASE-2)

## [Unreleased] — 2026-11-22

### Añadido

- Motor de optimizacion puro Python (OPT-002)

## [Unreleased] — 2026-11-22

### Añadido

- Evaluate base human body providers (BASE-001)

## [Unreleased] — 2026-11-22

### Añadido

- Primera pieza funcional de punta a punta (CORE-001)

## [Unreleased] — 2026-11-22

### Añadido

- Batería de calidad en verde (QA-001)

## [Unreleased] — 2026-11-22

### Añadido

- Phase 0: Technical Research (PHASE-0)

## [Unreleased] — 2026-11-22

### Añadido

- Qué se sabe ya y qué agentes hacen falta (ONBOARD-002)

## [Unreleased] — 2026-11-21

### Añadido

- Entender el proyecto (ONBOARD-001)

## [Unreleased] — 2026-11-21

### Añadido

- Decidir cómo se va a resolver (DESIGN-001)

## [Unreleased] — 2026-11-21

### Añadido

- Definir qué se quiere resolver (SCOPE-001)

## [Unreleased] — 2026-08-04

### Añadido

- protege app.__main__ para que importar el paquete no ejecute la CLI (FIX-001)

## [0.1.0] — 2026-08-04

### Añadido

- Arnés de trabajo: `AGENTS.md`, `init.sh`, `harness/` (backlog + progreso) y
  los cuatro subagentes (`lider`, `explorer`, `implementer`, `reviewer`).
- Sistema de 23 agentes Python en `agents/`, con contratos de rol y puerta de
  permisos (`agents/permissions.py`) para las acciones irreversibles.
- `agents/policy_guard.py` como política para las herramientas del asistente,
  sin cablear a ningún hook: se activa a mano (ver `AGENTS.md`).
- Vault de conocimiento en `vault/`, RAG local opcional y grafo con graphify.
- Paquete de ejemplo `app/` con su CLI y tests, `make check` en verde y CI.
