# lower_limb — Modelado de musculos del miembro inferior

**Esto es un esqueleto.** Lo generó `installer scaffold` y sus acciones no
hacen nada todavía: cada una devuelve `success=false` con lo que le falta en
`needs`. Mientras siga así, no le prometas al usuario que este agente resuelve
algo — lo que resuelve está por escribir en `agents/external/lower_limb_agent.py`.

## Qué falta antes de poder usarlo

1. Implementar sus acciones (`model`) en `agents/external/lower_limb_agent.py`.
2. Sustituir los tests generados en `agents/tests/test_lower_limb_agent.py`
   por tests de lo que la acción hace de verdad, no de que avisa de que no
   hace nada.
3. Repasar el contrato de abajo: lo escribió quien lanzó el scaffold en una
   línea, y `validate_contracts()` comprueba que no se pise con otro agente,
   no que sea verdad.

Borra esta sección cuando deje de ser cierta.

<!-- BEGIN AUTOGEN — lo regenera `make prompts-sync`; no lo edites a mano -->

## Acciones

| Acción | Argumentos |
|--------|------------|
| `run lower_limb model` | — |

## Límites

**Rol.** Modelado de musculos del miembro inferior

**Escribe en (nadie más toca esto):** agents/workspace/lower_limb/

<!-- END AUTOGEN -->
