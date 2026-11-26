"""
Tests de 'core_trunk', generados por `installer scaffold`.

Son la red mínima: que el agente esté registrado, que tenga contrato y que
sus acciones digan la verdad mientras sigan sin implementar. Cuando
implementes una acción, sustituye su test por uno que compruebe lo que hace.
"""

from __future__ import annotations

from agents.context import SharedContext
from agents.contracts import contract_for, validate_contracts
from agents.core.registry import agent_registry
from agents.external.core_trunk_agent import CoreTrunkAgent


def test_core_trunk_esta_registrado() -> None:
    assert "core_trunk" in agent_registry.all()


def test_core_trunk_tiene_contrato() -> None:
    contrato = contract_for("core_trunk")
    assert contrato is not None
    assert contrato.role


def test_core_trunk_no_rompe_los_contratos_del_equipo() -> None:
    assert validate_contracts(set(agent_registry.all())) == []


def test_model_admite_que_no_esta_implementada(context: SharedContext) -> None:
    resultado = CoreTrunkAgent(context=context).model()
    assert not resultado.success
    assert resultado.needs
