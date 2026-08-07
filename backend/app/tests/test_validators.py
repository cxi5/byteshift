"""
Testes dos utilitários de validação (app/core/validators.py).

Esses testes existem por causa de uma auditoria de código: os bugs
cobertos aqui (NaN, infinito, overflow) eram silenciosos antes da
correção — passavam pela validação sem erro nenhum e geravam resultados
inválidos. Como a validação agora é centralizada, corrigir aqui corrige
os 4 serviços ao mesmo tempo.
"""

import math

import pytest

from app.core.exceptions import InvalidValueError, NegativeValueError
from app.core.validators import round_result, validate_non_negative


class TestValidateNonNegative:
    def test_valor_positivo_nao_levanta_erro(self):
        validate_non_negative(10)  # não deve levantar nada

    def test_valor_zero_nao_levanta_erro(self):
        validate_non_negative(0)  # zero é um valor de entrada válido

    def test_valor_negativo_levanta_negative_value_error(self):
        with pytest.raises(NegativeValueError):
            validate_non_negative(-1)

    def test_nan_levanta_invalid_value_error(self):
        # sem essa checagem, NaN < 0 é False em Python e passaria batido
        with pytest.raises(InvalidValueError):
            validate_non_negative(float("nan"))

    def test_infinito_positivo_levanta_invalid_value_error(self):
        with pytest.raises(InvalidValueError):
            validate_non_negative(float("inf"))

    def test_infinito_negativo_levanta_invalid_value_error(self):
        with pytest.raises(InvalidValueError):
            validate_non_negative(float("-inf"))

    def test_texto_levanta_invalid_value_error(self):
        with pytest.raises(InvalidValueError):
            validate_non_negative("10")  # type: ignore[arg-type]

    def test_booleano_levanta_invalid_value_error(self):
        # bool é subclasse de int em Python (True == 1) -- sem a checagem
        # explícita, um True passaria como se fosse o número 1
        with pytest.raises(InvalidValueError):
            validate_non_negative(True)  # type: ignore[arg-type]


class TestRoundResult:
    def test_arredonda_na_precisao_padrao(self):
        assert round_result(1.123456789) == 1.123457

    def test_arredonda_em_precisao_customizada(self):
        assert round_result(1.987, precision=1) == 2.0

    def test_valor_infinito_levanta_invalid_value_error(self):
        # simula o overflow: uma multiplicação de float que já resultou
        # em infinito antes de chegar no arredondamento
        with pytest.raises(InvalidValueError):
            round_result(math.inf)
