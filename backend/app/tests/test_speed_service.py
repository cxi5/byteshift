"""
Testes do speed_service.

Cobre: valores conhecidos, decimal vs binário, casos-limite e erros.
"""

import pytest

from app.core.validators import NegativeValueError
from app.services.speed_service import InvalidUnitError, convert_speed


class TestValoresConhecidos:
    def test_1_megabyte_por_segundo_em_kilobyte_por_segundo(self):
        assert convert_speed(1, "megabyte_per_second")["kilobyte_per_second"] == 1000.0

    def test_100_megabyte_por_segundo_em_byte_por_segundo(self):
        assert convert_speed(100, "megabyte_per_second")["byte_per_second"] == 100_000_000.0


class TestDecimalVsBinario:
    def test_1024_kibibyte_por_segundo_igual_1_mebibyte_por_segundo_exato(self):
        assert convert_speed(1024, "kibibyte_per_second")["mebibyte_per_second"] == 1.0

    def test_100_megabyte_por_segundo_nao_bate_exato_em_mebibyte_por_segundo(self):
        result = convert_speed(100, "megabyte_per_second")
        assert result["mebibyte_per_second"] == pytest.approx(95.367432)
        assert result["mebibyte_per_second"] != 100.0


class TestValoresLimite:
    def test_valor_zero(self):
        result = convert_speed(0, "megabyte_per_second")
        assert all(v == 0.0 for v in result.values())

    def test_valor_muito_grande(self):
        result = convert_speed(1_000_000, "gigabyte_per_second")
        assert result["byte_per_second"] == 1_000_000 * 1_000**3


class TestErros:
    def test_unidade_inexistente_levanta_invalid_unit_error(self):
        with pytest.raises(InvalidUnitError):
            convert_speed(1, "lightyear_per_second")

    def test_valor_negativo_levanta_negative_value_error(self):
        with pytest.raises(NegativeValueError):
            convert_speed(-1, "byte_per_second")
