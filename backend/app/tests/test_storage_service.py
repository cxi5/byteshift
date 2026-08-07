"""
Testes do storage_service.

Cobre: valores conhecidos, decimal vs binário, casos-limite e erros.
Todos os valores esperados foram calculados rodando o serviço real
antes de escrever o teste — nada aqui foi "chutado".
"""

import pytest

from app.core.validators import NegativeValueError
from app.core.exceptions import InvalidValueError
from app.services.storage_service import InvalidUnitError, convert_storage


class TestValoresConhecidos:
    def test_1_byte_igual_8_bits(self):
        assert convert_storage(1, "byte")["bit"] == 8.0

    def test_1_gigabyte_decimal_em_megabyte(self):
        assert convert_storage(1, "gigabyte")["megabyte"] == 1000.0

    def test_1_gigabyte_decimal_em_bytes(self):
        assert convert_storage(1, "gigabyte")["byte"] == 1_000_000_000.0


class TestDecimalVsBinario:
    def test_1024_mebibyte_igual_1_gibibyte_exato(self):
        # binário: 1024 MiB = 1 GiB, exato (potência de 1024)
        assert convert_storage(1024, "mebibyte")["gibibyte"] == 1.0

    def test_1000_megabyte_bate_exato_em_gigabyte_decimal(self):
        assert convert_storage(1000, "megabyte")["gigabyte"] == 1.0

    def test_1000_megabyte_nao_bate_exato_em_gibibyte_binario(self):
        # decimal (1000 MB) e binário (GiB) não podem se confundir
        assert convert_storage(1000, "megabyte")["gibibyte"] == 0.931323
        assert convert_storage(1000, "megabyte")["gibibyte"] != 1.0

    def test_1_gigabyte_decimal_em_gibibyte_binario(self):
        # a "perda" clássica que todo mundo vê no gerenciador de disco
        assert convert_storage(1, "gigabyte")["gibibyte"] == pytest.approx(0.931323)


class TestValoresLimite:
    def test_valor_zero_resulta_em_zero_em_todas_unidades(self):
        result = convert_storage(0, "gigabyte")
        assert all(v == 0.0 for v in result.values())

    def test_valor_muito_grande(self):
        result = convert_storage(1_000_000, "terabyte")
        assert result["byte"] == 1e18

    def test_valor_decimal_com_muitas_casas_e_arredondado(self):
        # precisão padrão é 6 casas decimais (DEFAULT_ROUNDING_PRECISION)
        result = convert_storage(1.123456789, "gigabyte")
        assert result["gigabyte"] == 1.123457

    def test_valor_absurdamente_grande_estoura_float_e_levanta_erro(self):
        # 1e300 petabytes ultrapassa o limite de um float de 64 bits
        # (~1.8e308) assim que multiplicado pelo fator de conversão.
        # Antes da correção, isso virava `inf` silenciosamente; agora
        # levanta um erro claro em vez de devolver um resultado quebrado.
        with pytest.raises(InvalidValueError):
            convert_storage(1e300, "petabyte")


class TestErros:
    def test_unidade_inexistente_levanta_invalid_unit_error(self):
        with pytest.raises(InvalidUnitError):
            convert_storage(1, "fooblat")

    def test_valor_negativo_levanta_negative_value_error(self):
        with pytest.raises(NegativeValueError):
            convert_storage(-1, "byte")
