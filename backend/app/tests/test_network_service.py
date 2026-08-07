"""
Testes do network_service.

Cobre: valores conhecidos, garantia de que não existe unidade binária
(padrão da indústria é sempre decimal), casos-limite e erros.
"""

import pytest

from app.core.validators import NegativeValueError
from app.services.network_service import InvalidUnitError, convert_network


class TestValoresConhecidos:
    def test_1000_kilobit_por_segundo_igual_1_megabit_por_segundo(self):
        assert convert_network(1000, "kilobit_per_second")["megabit_per_second"] == 1.0

    def test_300_megabit_por_segundo_em_gigabit_por_segundo(self):
        assert convert_network(300, "megabit_per_second")["gigabit_per_second"] == 0.3


class TestSemUnidadeBinaria:
    def test_unidade_binaria_nao_existe_em_rede(self):
        # Rede segue padrão da indústria: só decimal. kibibit_per_second
        # não deve existir nessa tabela — se existisse, seria um erro de
        # modelagem (confundindo com o gênero Velocidade).
        with pytest.raises(InvalidUnitError):
            convert_network(1, "kibibit_per_second")


class TestValoresLimite:
    def test_valor_zero(self):
        result = convert_network(0, "megabit_per_second")
        assert all(v == 0.0 for v in result.values())

    def test_valor_muito_grande(self):
        result = convert_network(1_000_000, "gigabit_per_second")
        assert result["bit_per_second"] == 1_000_000 * 1_000**3


class TestErros:
    def test_unidade_inexistente_levanta_invalid_unit_error(self):
        with pytest.raises(InvalidUnitError):
            convert_network(1, "carrier_pigeon_per_second")

    def test_valor_negativo_levanta_negative_value_error(self):
        with pytest.raises(NegativeValueError):
            convert_network(-1, "bit_per_second")
