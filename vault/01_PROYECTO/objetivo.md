# Objetivo — FORMA

## Problema

Los gemelos digitales humanos disponibles hoy son, en su mayoría, avatares visuales estáticos o parametrizaciones superficiales de una malla. No existe un modelo con **capas independientes y reemplazables** (esqueleto, sistema muscular, tejido adiposo, piel/superficie) que se pueda modificar por componente sin perder la coherencia del resto, con persistencia y versionado, y con estimación de incertidumbre sobre los parámetros inferidos. FORMA resuelve eso: un gemelo digital persistente por persona, anatómicamente restringido, reutilizable en múltiples aplicaciones.

## Usuario / consumidor

Desarrolladores, investigadores y aplicaciones (fitness, moda, ergonomía, educación, body art, etc.) que necesitan un gemelo digital humano individualizado. El núcleo anatómico no depende del motor de render ni de la interfaz: se consume como biblioteca/servicio.

## Criterio de hecho

Verificable por comando: `make check` termina en verde (lint + typecheck + tests + arnés) y `./init.sh` imprime `ENTORNO LISTO` sin avisos. A nivel de producto: un gemelo se reconstruye a partir de 3 fotografías, persiste, permite modificar músculos concretos (deltoides, pectoral, bíceps, abdomen) y guardar/comparar configuraciones (MVP-001).

## Fuera de alcance

- Diagnóstico médico, estimación clínica o cualquier uso que requiera validación sanitaria.
- Renderizado fotorealista en tiempo real / motor de juego: el núcleo anatómico no depende del render.
- Modelado de no-humanos (animales, criaturas ficticias) y reconstrucción multi-persona en una misma escena.
- Almacenamiento multi-usuario en la nube y autenticación: la persistencia es local al gemelo.
