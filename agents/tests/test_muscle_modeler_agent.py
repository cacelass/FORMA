"""
Tests de 'muscle_modeler', generados por `installer scaffold`.

Son la red mínima: que el agente esté registrado, que tenga contrato y que
sus acciones digan la verdad mientras sigan sin implementar. Cuando
implementes una acción, sustituye su test por uno que compruebe lo que hace.
"""

from __future__ import annotations

from agents.context import SharedContext
from agents.contracts import contract_for, validate_contracts
from agents.core.registry import agent_registry
from agents.external.muscle_modeler_agent import MuscleModelerAgent


def test_muscle_modeler_esta_registrado() -> None:
    assert "muscle_modeler" in agent_registry.all()


def test_muscle_modeler_tiene_contrato() -> None:
    contrato = contract_for("muscle_modeler")
    assert contrato is not None
    assert contrato.role


def test_muscle_modeler_no_rompe_los_contratos_del_equipo() -> None:
    assert validate_contracts(set(agent_registry.all())) == []


def test_model_muscle_admite_que_no_esta_implementada(context: SharedContext) -> None:
    resultado = MuscleModelerAgent(context=context).model_muscle()
    assert not resultado.success
    assert resultado.needs
