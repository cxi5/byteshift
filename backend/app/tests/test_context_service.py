"""
Testes do context_service (Fase 8 — conversões contextuais).

Todos os valores esperados foram calculados rodando o serviço real
antes de escrever o teste, igual nos outros arquivos de teste.
"""

import pytest

from app.core.exceptions import InvalidUnitError, InvalidValueError, NegativeValueError
from app.services.context_service import (
    calculate_download_time,
    calculate_files_that_fit,
    calculate_transfer_time,
)


class TestDownloadTime:
    def test_1_gigabyte_a_100_megabit_por_segundo(self):
        result = calculate_download_time(1, "gigabyte", 100, "megabit_per_second")
        assert result["seconds"] == 80.0
        assert result["human_readable"] == "1min 20s"

    def test_tempo_menor_que_1_segundo_mostra_casas_decimais(self):
        result = calculate_download_time(1, "megabyte", 1, "gigabit_per_second")
        assert result["seconds"] < 1
        assert result["human_readable"].endswith("s")

    def test_tamanho_zero_resulta_em_tempo_zero(self):
        result = calculate_download_time(0, "gigabyte", 100, "megabit_per_second")
        assert result["seconds"] == 0.0

    def test_velocidade_zero_levanta_invalid_value_error(self):
        with pytest.raises(InvalidValueError):
            calculate_download_time(1, "gigabyte", 0, "megabit_per_second")

    def test_valor_negativo_levanta_negative_value_error(self):
        with pytest.raises(NegativeValueError):
            calculate_download_time(-1, "gigabyte", 100, "megabit_per_second")

    def test_unidade_de_armazenamento_invalida(self):
        with pytest.raises(InvalidUnitError):
            calculate_download_time(1, "unidade_fake", 100, "megabit_per_second")

    def test_unidade_de_rede_invalida(self):
        with pytest.raises(InvalidUnitError):
            calculate_download_time(1, "gigabyte", 100, "unidade_fake")

    def test_nao_aceita_unidade_de_velocidade_no_lugar_de_rede(self):
        # megabyte_per_second é do gênero Velocidade, não Rede — não pode
        # ser usada aqui, isso confundiria os dois cenários
        with pytest.raises(InvalidUnitError):
            calculate_download_time(1, "gigabyte", 100, "megabyte_per_second")


class TestTransferTime:
    def test_1_gigabyte_a_30_megabyte_por_segundo(self):
        result = calculate_transfer_time(1, "gigabyte", 30, "megabyte_per_second")
        assert result["seconds"] == 33.333333
        assert result["human_readable"] == "33s"

    def test_velocidade_zero_levanta_invalid_value_error(self):
        with pytest.raises(InvalidValueError):
            calculate_transfer_time(1, "gigabyte", 0, "megabyte_per_second")

    def test_nao_aceita_unidade_de_rede_no_lugar_de_velocidade(self):
        # o inverso do teste em TestDownloadTime — megabit_per_second é
        # de Rede, não pode ser usado em transferência local
        with pytest.raises(InvalidUnitError):
            calculate_transfer_time(1, "gigabyte", 100, "megabit_per_second")


class TestFilesThatFit:
    def test_fotos_de_5mb_em_cartao_de_29_8_gibibyte(self):
        result = calculate_files_that_fit(5, "megabyte", 29.802322, "gibibyte")
        assert result["files_that_fit"] == 6399
        assert result["leftover_bytes"] == pytest.approx(4999583.715328, abs=1e-3)

    def test_sobra_e_convertida_em_todas_unidades_de_armazenamento(self):
        result = calculate_files_that_fit(5, "megabyte", 29.802322, "gibibyte")
        assert "megabyte" in result["leftover_in_units"]
        assert "gibibyte" in result["leftover_in_units"]

    def test_arquivo_maior_que_a_capacidade_resulta_em_zero_arquivos(self):
        result = calculate_files_that_fit(500, "gigabyte", 1, "gibibyte")
        assert result["files_that_fit"] == 0

    def test_tamanho_de_arquivo_zero_levanta_invalid_value_error(self):
        with pytest.raises(InvalidValueError):
            calculate_files_that_fit(0, "megabyte", 32, "gibibyte")

    def test_nao_aceita_unidade_anunciada_no_lugar_da_real(self):
        # gigabyte é a unidade ANUNCIADA (decimal) — aqui só a REAL
        # (binária) faz sentido, porque é o espaço que sobra de verdade
        with pytest.raises(InvalidUnitError):
            calculate_files_that_fit(5, "megabyte", 32, "gigabyte")

    def test_valor_negativo_levanta_negative_value_error(self):
        with pytest.raises(NegativeValueError):
            calculate_files_that_fit(5, "megabyte", -32, "gibibyte")
