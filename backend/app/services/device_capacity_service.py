"""
Serviço de Capacidade de Dispositivos.

Único módulo que expõe essa conversão pra fora. É o único lugar do
projeto que passa as tabelas DEVICE_CAPACITY_ADVERTISED_UNITS e
DEVICE_CAPACITY_REAL_UNITS pro motor de conversão — mesmo reaproveitando
fatores de byte que "parecem" iguais aos de Armazenamento, são tabelas
diferentes por design.

Diferente dos outros gêneros, aqui a conversão NÃO é simétrica: a entrada
sempre vem em unidade ANUNCIADA (decimal, o que o fabricante escreve na
caixa) e a saída é sempre em unidades REAIS (binário, o que o sistema
operacional de fato exibe). Não faz sentido converter "anunciado -> anunciado".
"""

from app.core.constants import DEVICE_CAPACITY_ADVERTISED_UNITS, DEVICE_CAPACITY_REAL_UNITS
from app.core.conversion_engine import convert_via_base
from app.core.exceptions import InvalidUnitError  # reexportado para compatibilidade

__all__ = ["convert_device_capacity", "InvalidUnitError"]


def convert_device_capacity(value: float, from_unit: str) -> dict[str, float]:
    """
    Converte `value`, anunciado em `from_unit` (decimal, ex: "gigabyte"),
    para todas as unidades REAIS (binário) exibidas pelo sistema
    operacional. Toda conversão passa pela unidade-base interna (byte).
    """
    return convert_via_base(
        value=value,
        from_unit=from_unit,
        source_table=DEVICE_CAPACITY_ADVERTISED_UNITS,
        target_table=DEVICE_CAPACITY_REAL_UNITS,
        genre_label="capacidade de dispositivo",
    )
