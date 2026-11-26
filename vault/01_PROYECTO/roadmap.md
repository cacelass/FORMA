# Roadmap — FORMA

> El backlog vivo es `harness/featureslist.json`. Esto es la vista larga: lo
> que se quiere conseguir, no la tarea de hoy.

## Fase actual

- [x] `SCOPE-001` — definir qué se quiere resolver
- [x] `DESIGN-001` — decidir cómo se va a resolver
- [x] `CORE-001` — primera pieza funcional de punta a punta
- [x] `QA-001` — batería de calidad y CI en verde
- [x] `PHASE-0` — investigación técnica
- [x] `BASE-001` — evaluación de proveedores base
- [x] `PHASE-2` — anatomía paramétrica (modelo puro Python)
- [x] `PHASE-6` — módulos de aplicación (fitness, fashion, body_art)

## Bloqueadas por infraestructura 3D

- [ ] `PHASE-1` — fundación 3D (BlenderBridge)
- [ ] `PHASE-3` — reconstrucción desde fotos
- [ ] `PHASE-4` — superficie y piel
- [ ] `PHASE-5` — motor de interacción
- [ ] `PHASE-7` — interfaz de plataforma
- [ ] `MVP-001` — gemelo digital desde 3 fotos
- [ ] `OPT-001` — motor de optimización para reconstrucción (base en OPT-002)

## Próximos pasos

- [ ] Instalar proveedor base (BASE-001) y desbloquear PHASE-1.
- [ ] Rellenar `docs/spec/FORMA.md` con la especificación completa.
- [ ] Empaquetado o despliegue, si aplica.

## Historial de decisiones

| Fecha | Decisión | Contexto |
|-------|----------|----------|
| 2026-11-22 | JSON como formato de persistencia del gemelo | IMPROVE-001, forma/persistence/store.py |
| 2026-11-22 | BaseBodyProvider como abstracción del proveedor base | BASE-001 |
