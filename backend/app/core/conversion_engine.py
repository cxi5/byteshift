"""
Motor de conversão genérico, usado internamente pelos serviços.

Importante: isso NÃO é a "função genérica que converte tudo" que a regra
de ouro do projeto proíbe. Este módulo não guarda nenhuma tabela de
unidades — cada serviço continua isolado e é o único responsável por
escolher e passar a SUA PRÓPRIA tabela. O que esse módulo evita é repetir
a mesma mecânica de busca, validação e loop em quatro arquivos diferentes,
o que facilita adicionar um quinto gênero no futuro sem copiar e colar código.
"""

from app.core.constants import UnitDefinition
from app.core.exceptions import InvalidUnitError
from app.core.validators import round_result, validate_non_negative


def get_unit_or_raise(
    units_table: dict[str, UnitDefinition],
    unit_key: str,
    genre_label: str,
) -> UnitDefinition:
    """Busca uma unidade na tabela informada ou levanta um erro claro com as opções válidas."""
    unit = units_table.get(unit_key)
    if unit is None:
        valid = ", ".join(sorted(units_table))
        raise InvalidUnitError(
            f"Unidade de {genre_label} inválida: '{unit_key}'. Válidas: {valid}"
        )
    return unit


def convert_via_base(
    value: float,
    from_unit: str,
    source_table: dict[str, UnitDefinition],
    target_table: dict[str, UnitDefinition],
    genre_label: str,
) -> dict[str, float]:
    """
    Converte `value`, informado em `from_unit` (buscado em `source_table`),
    para todas as unidades de `target_table`.

    Na maioria dos gêneros, `source_table` e `target_table` são a mesma
    tabela — a conversão é simétrica (qualquer unidade pode ser entrada
    ou saída). Em Capacidade de Dispositivos elas são tabelas diferentes
    de propósito: a entrada é sempre em unidade anunciada e a saída
    sempre em unidade real.

    Toda conversão passa pela unidade-base do gênero — nunca unidade A
    vira unidade B diretamente.
    """
    validate_non_negative(value)
    source = get_unit_or_raise(source_table, from_unit, genre_label)

    value_in_base = value * source.factor_to_base

    results: dict[str, float] = {}
    for key, unit in target_table.items():
        results[key] = round_result(value_in_base / unit.factor_to_base)

    return results
