"""
Serviço de conversão de Armazenamento.

Único módulo que expõe conversão de Armazenamento pra fora. É o único
lugar do projeto que passa a tabela STORAGE_UNITS pro motor de conversão
— isolamento total, mesmo usando um motor compartilhado por baixo.
"""

from app.core.constants import STORAGE_UNITS
from app.core.conversion_engine import convert_via_base
from app.core.exceptions import InvalidUnitError  # reexportado para compatibilidade

__all__ = ["convert_storage", "InvalidUnitError"]


def convert_storage(value: float, from_unit: str) -> dict[str, float]:
    """
    Converte `value`, informado em `from_unit`, para todas as unidades
    de Armazenamento. Toda conversão passa pela unidade-base interna (bit).
    """
    return convert_via_base(
        value=value,
        from_unit=from_unit,
        source_table=STORAGE_UNITS,
        target_table=STORAGE_UNITS,
        genre_label="armazenamento",
    )
