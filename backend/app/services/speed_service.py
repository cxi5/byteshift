"""
Serviço de conversão de Velocidade de transferência de arquivos.

Único módulo que expõe conversão de Velocidade pra fora. É o único
lugar do projeto que passa a tabela SPEED_UNITS pro motor de conversão.
"""

from app.core.constants import SPEED_UNITS
from app.core.conversion_engine import convert_via_base
from app.core.exceptions import InvalidUnitError  # reexportado para compatibilidade

__all__ = ["convert_speed", "InvalidUnitError"]


def convert_speed(value: float, from_unit: str) -> dict[str, float]:
    """
    Converte `value`, informado em `from_unit`, para todas as unidades
    de Velocidade de transferência. Toda conversão passa pela
    unidade-base interna (byte/s).
    """
    return convert_via_base(
        value=value,
        from_unit=from_unit,
        source_table=SPEED_UNITS,
        target_table=SPEED_UNITS,
        genre_label="velocidade",
    )
