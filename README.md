# FORMA

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)
![Version](https://img.shields.io/badge/Version-0.1.11-green)
![Author](https://img.shields.io/badge/Author-cacelass-blueviolet)

> Parametric Human Digital Twin Platform.

FORMA es una plataforma modular para reconstruir, representar,
modificar, simular y analizar cuerpos humanos individuales mediante
gemelos digitales 3D persistentes y anatómicamente restringidos.

Un gemelo digital de FORMA no es solo un avatar visual: es un modelo
parametrizado con capas independientes (esqueleto, músculos, tejido
adiposo, piel/superficie) que puede modificarse por componente sin
perder la coherencia del resto.

**Principio central:** una persona, un gemelo digital persistente,
múltiples aplicaciones independientes.

FORMA NO se limita a fitness, bodybuilding, ropa, tatuajes, belleza
o moda: esas son aplicaciones de una plataforma mucho más amplia de
modelado y simulación humana.

---

## Tabla de contenidos

- [Objetivos](#objetivos)
- [Arquitectura por capas](#arquitectura-por-capas)
- [Inicio rápido](#inicio-rápido)
- [Estructura del proyecto](#estructura-del-proyecto)
- [El arnés](#el-arnés)
- [Roadmap](#roadmap)

---

## Objetivos

1. Reconstruir un cuerpo humano individualizado en 3D.
2. Estimar proporciones anatómicas y medidas antropométricas.
3. Representar esqueleto y sistema muscular con componentes independientes.
4. Modelar tejido adiposo subcutáneo y geometría externa.
5. Aplicar piel y materiales de superficie realistas.
6. Soportar modificaciones anatómicas preservando consistencia geométrica.
7. Soportar posing y deformación.
8. Permitir uso del gemelo en simulación y visualización externa.
9. Soportar interacción realista con objetos externos.
10. Persistencia y versionado.
11. Estimación de incertidumbre de parámetros inferidos.
12. Extensibilidad a aplicaciones no definidas aún.

---

## Arquitectura por capas

| Capa | Responsabilidad |
|------|-----------------|
| 1. Esqueleto | Proporciones óseas, articulaciones, restricciones, asimetrías |
| 2. Sistema muscular | Músculos individuales parametrizados (origen/inserción, volumen, longitud, grosor) |
| 3. Tejido adiposo | Grasa subcutánea regional, separando medido de estimado |
| 4. Piel y superficie | Superficie externa, UV, materiales, SSS |
| 5. Objetos externos | Ropa, tatuajes, accesorios, equipos (independiente del modelo anatómico) |

Cada capa es independiente y reemplazable. El núcleo anatómico no depende
del motor de render ni de la interfaz.

---

## Inicio rápido

```bash
make setup     # uv sync --extra dev + hooks de pre-commit
make init      # la puerta: ¿el proyecto está sano?
make run       # ejecuta el paquete de ejemplo
make check     # lint + typecheck + test + arnés
```

Y para arrancar el ciclo de trabajo en tu asistente:

> Lee `AGENTS.md` y sigue el protocolo: ejecuta `./init.sh`, lee
> `harness/progress/` y elige la primera feature pendiente.

---

## Ejecución

El punto de entrada del paquete es la CLI `forma`:

```bash
uv run python -m forma hello --name FORMA
```

Salida esperada:

```
Hola, FORMA.
```

Código de salida `0`. Sin subcomando, argparse devuelve código `2` (error de uso).
Para la versión: `uv run python -m forma --version`.

---

## Estructura del proyecto

```
forma/                 ← TU código (paquete principal)
tests/                 ← tus tests
agents/                ← el sistema de agentes (arnés)
harness/               ← backlog con criterios de aceptación + progreso
vault/                 ← conocimiento estable del proyecto (Obsidian)
docs/                  ← Sphinx + PRD
```

La especificación completa del proyecto está en
`docs/spec/FORMA.md` (pendiente de crear) o en el documento original.

---

## El arnés

Este repositorio incluye el arnés de agentes de MeshHarmes: puerta de
entrada (`init.sh`), backlog con criterios de aceptación, memoria fuera de
la ventana de contexto y puerta de permisos. Ver `AGENTS.md`.

---

## Roadmap

- **PHASE 0** — Investigación técnica (modelos base, licencias, arquitectura).
- **PHASE 1** — Fundación 3D (BlenderBridge, modelo base, render).
- **PHASE 2** — Anatomía paramétrica (esqueleto, músculos, deformación).
- **PHASE 3** — Reconstrucción por foto (pose, landmarks, fitting).
- **PHASE 4** — Superficie y piel.
- **PHASE 5** — Motor de interacción general.
- **PHASE 6** — Módulos de aplicación.
- **PHASE 7** — Interfaz de plataforma.

**MVP:** 3 fotos → gemelo digital 3D persistente con músculos editables
independientemente.

---

## Licencia

MIT. Ver `LICENSE`.
