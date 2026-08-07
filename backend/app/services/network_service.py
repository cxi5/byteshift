"""
Serviço de conversão de banda de Rede (internet, download/upload).

Único módulo que expõe conversão de Rede pra fora. É o único lugar do
projeto que passa a tabela NETWORK_UNITS pro motor de conversão.

Diferente de Velocidade (transferência de arquivos), Rede segue o padrão
da indústria de sempre usar prefixos decimais — por isso NETWORK_UNITS
não tem variantes binárias.
"""

from app.core.constants import NETWORK_UNITS
from app.core.conversion_engine import convert_via_base
from app.core.exceptions import InvalidUnitError  # reexportado para compatibilidade

__all__ = ["convert_network", "InvalidUnitError"]


def convert_network(value: float, from_unit: str) -> dict[str, float]:
    """
    Converte `value`, informado em `from_unit`, para todas as unidades
    de banda de Rede. Toda conversão passa pela unidade-base interna (bit/s).
    """
    return convert_via_base(
        value=value,
        from_unit=from_unit,
        source_table=NETWORK_UNITS,
        target_table=NETWORK_UNITS,
        genre_label="rede",
    )
