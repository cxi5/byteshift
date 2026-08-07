"""
Utilitários de validação e arredondamento, compartilhados pelos serviços.

Este módulo NÃO conhece unidades nem faz conversão — só valida e formata
números. A lógica de conversão em si continua isolada em cada serviço.
"""

import math

from app.core.constants import DEFAULT_ROUNDING_PRECISION
from app.core.exceptions import InvalidValueError, NegativeValueError


def validate_non_negative(value: float) -> None:
    """
    Garante que `value` é um número finito e não-negativo.

    A checagem de NaN e infinito existe de propósito: sem ela, esses
    valores passariam pela validação sem erro nenhum (em Python,
    `float('nan') < 0` é `False`) e contaminariam o resultado inteiro da
    conversão de forma silenciosa — exatamente o tipo de bug que este
    projeto quer evitar.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InvalidValueError(f"Valor inválido: {value!r}. Esperado um número.")

    if not math.isfinite(value):
        raise InvalidValueError(
            f"Valor inválido: {value}. Não são aceitos NaN nem infinito."
        )

    if value < 0:
        raise NegativeValueError(
            f"Valor inválido: {value}. Conversões não aceitam números negativos."
        )


def round_result(value: float, precision: int = DEFAULT_ROUNDING_PRECISION) -> float:
    """
    Arredonda o resultado de uma conversão, garantindo que ele continua
    representável.

    Se o valor de entrada for grande o bastante pra multiplicação por um
    fator de conversão estourar o limite de um float de 64 bits, o
    resultado vira infinito silenciosamente em Python (não levanta
    exceção nenhuma). Aqui isso é convertido num erro explícito, porque
    infinito não é um valor de JSON válido e quebraria a resposta da API
    sem explicar o motivo.
    """
    if not math.isfinite(value):
        raise InvalidValueError(
            "O resultado da conversão ultrapassa o limite representável "
            "(overflow). Use um valor de entrada menor."
        )
    return round(value, precision)
