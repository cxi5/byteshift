"""
Testes do device_capacity_service.

Cobre: o caso clássico do "sumiço" de espaço (anunciado vs real),
garantia de que unidades REAIS não são aceitas como entrada, casos-limite
e erros.
"""

import pytest

from app.core.validators import NegativeValueError
from app.services.device_capacity_service import InvalidUnitError, convert_device_capacity


class TestValoresConhecidos:
    def test_1_terabyte_anunciado_em_gibibyte_real(self):
        # o clássico "HD de 1TB mostra 931GB no Windows"
        result = convert_device_capacity(1, "terabyte")
        assert result["gibibyte"] == pytest.approx(931.322575)

    def test_256_gigabyte_anunciado_em_gibibyte_real(self):
        # SSD de 256GB que o SO mostra como ~238GB
        result = convert_device_capacity(256, "gigabyte")
        assert result["gibibyte"] == pytest.approx(238.418579)


class TestEntradaSomenteDecimal:
    def test_unidade_real_nao_e_entrada_valida(self):
        # gibibyte é unidade de SAÍDA (real), não pode ser usada como
        # unidade de ENTRADA (anunciada) — a conversão não é simétrica
        with pytest.raises(InvalidUnitError):
            convert_device_capacity(1, "gibibyte")


class TestValoresLimite:
    def test_valor_zero(self):
        result = convert_device_capacity(0, "gigabyte")
        assert all(v == 0.0 for v in result.values())

    def test_valor_muito_grande(self):
        result = convert_device_capacity(1_000_000, "terabyte")
        assert result["tebibyte"] == pytest.approx(909494.701773, abs=1e-3)


class TestErros:
    def test_unidade_inexistente_levanta_invalid_unit_error(self):
        with pytest.raises(InvalidUnitError):
            convert_device_capacity(1, "fooblat")

    def test_valor_negativo_levanta_negative_value_error(self):
        with pytest.raises(NegativeValueError):
            convert_device_capacity(-1, "gigabyte")
