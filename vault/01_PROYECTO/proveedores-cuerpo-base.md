# Comparativa de proveedores de cuerpo base — FORMA (BASE-001)

| Proveedor | Topología | Rigging | Extensibilidad | Licencia | Notas |
|-----------|-----------|---------|----------------|----------|-------|
| SMPL-X | Paramétrico (PCA) | Esqueleto completo + manos/cara | Alta (shape/pose params) | Académica (no comercial) | Mejor para investigación y fitting |
| MakeHuman | Malla paramétrica | Básico | Media (targets) | AGPL / CC0 (assets) | Buena para uso comercial con cuidado |
| MB-Lab | Basado en MakeHuman | Avanzado | Media | GPL | Plugin de Blender |
| Blender-native (metarig + sculpt) | Libre | Manual | Total | Blender (GPL) | Máximo control, más trabajo |

## Recomendación

- **Investigación / prototipo:** SMPL-X (mejor ajuste a fotos, literatura abundante).
- **Producto comercial:** MakeHuman o Blender-native para evitar restricciones de licencia académica.
- **Encapsular** siempre tras `BaseBodyProvider` (forma/providers/base_body_provider.py) para poder sustituir sin tocar el núcleo.

## Licencias (resumen)

- SMPL-X: uso académico no comercial por defecto; licencia comercial disponible.
- MakeHuman: código AGPL; assets CC0.
- MB-Lab: GPL.
- Blender: GPL (el runtime de Blender impone GPL al código que corre dentro de él).

## Decisión diferida

La elección final se toma en PHASE-1, tras validar el pipeline de reconstrucción con el proveedor candidato.
