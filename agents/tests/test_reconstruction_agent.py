"""
Tests de 'reconstruction', generados por `installer scaffold`.

Son la red mínima: que el agente esté registrado, que tenga contrato y que
sus acciones digan la verdad mientras sigan sin implementar. Cuando
implementes una acción, sustituye su test por uno que compruebe lo que hace.
"""

from __future__ import annotations

from agents.context import SharedContext
from agents.contracts import contract_for, validate_contracts
from agents.core.registry import agent_registry
from agents.external.reconstruction_agent import ReconstructionAgent


def test_reconstruction_esta_registrado() -> None:
    assert "reconstruction" in agent_registry.all()


def test_reconstruction_tiene_contrato() -> None:
    contrato = contract_for("reconstruction")
    assert contrato is not None
    assert contrato.role


def test_reconstruction_no_rompe_los_contratos_del_equipo() -> None:
    assert validate_contracts(set(agent_registry.all())) == []


def test_reconstruct_admite_que_no_esta_implementada(context: SharedContext) -> None:
    resultado = ReconstructionAgent(context=context).reconstruct()
    assert not resultado.success
    assert resultado.needs
