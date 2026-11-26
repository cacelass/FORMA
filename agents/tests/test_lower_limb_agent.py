"""
Tests de 'lower_limb', generados por `installer scaffold`.

Son la red mínima: que el agente esté registrado, que tenga contrato y que
sus acciones digan la verdad mientras sigan sin implementar. Cuando
implementes una acción, sustituye su test por uno que compruebe lo que hace.
"""

from __future__ import annotations

from agents.context import SharedContext
from agents.contracts import contract_for, validate_contracts
from agents.core.registry import agent_registry
from agents.external.lower_limb_agent import LowerLimbAgent


def test_lower_limb_esta_registrado() -> None:
    assert "lower_limb" in agent_registry.all()


def test_lower_limb_tiene_contrato() -> None:
    contrato = contract_for("lower_limb")
    assert contrato is not None
    assert contrato.role


def test_lower_limb_no_rompe_los_contratos_del_equipo() -> None:
    assert validate_contracts(set(agent_registry.all())) == []


def test_model_admite_que_no_esta_implementada(context: SharedContext) -> None:
    resultado = LowerLimbAgent(context=context).model()
    assert not resultado.success
    assert resultado.needs
