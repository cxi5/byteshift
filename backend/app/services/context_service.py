"""
Serviço de conversões contextuais (Fase 8 do roadmap).

Diferente dos outros serviços, este combina DUAS tabelas de gêneros
diferentes numa única conta (ex: tamanho de arquivo + velocidade de
rede = tempo de download). Ainda assim, isso não vira uma função
genérica "converte tudo": cada cenário continua sendo uma função
própria e explícita sobre quais dois gêneros ela combina e por quê.
"""

import math

from app.core.constants import DEVICE_CAPACITY_REAL_UNITS, NETWORK_UNITS, SPEED_UNITS, STORAGE_UNITS
from app.core.conversion_engine import get_unit_or_raise
from app.core.exceptions import InvalidValueError
from app.core.validators import round_result, validate_non_negative
from app.services.storage_service import convert_storage


def _seconds_to_human_readable(seconds: float) -> str:
    """Formata segundos como '2h 15min 4s', omitindo as partes zeradas."""
    if seconds < 1:
        return f"{round(seconds, 2)}s"

    total = int(round(seconds))
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)

    parts = []
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}min")
    if secs or not parts:
        parts.append(f"{secs}s")
    return " ".join(parts)


def calculate_download_time(size_value: float, size_unit: str, rate_value: float, rate_unit: str) -> dict:
    """
    Tempo estimado de download/upload: tamanho do arquivo (Armazenamento)
    dividido pela velocidade de banda (Rede). Os dois gêneros já
    compartilham a mesma dimensão de base (bit), então a conta é direta,
    sem precisar converter entre bit e byte no meio do caminho.
    """
    validate_non_negative(size_value)
    validate_non_negative(rate_value)

    size_unit_def = get_unit_or_raise(STORAGE_UNITS, size_unit, "armazenamento")
    rate_unit_def = get_unit_or_raise(NETWORK_UNITS, rate_unit, "rede")

    if rate_value == 0:
        raise InvalidValueError("A velocidade de rede não pode ser zero — divisão por zero.")

    size_in_bits = size_value * size_unit_def.factor_to_base
    rate_in_bps = rate_value * rate_unit_def.factor_to_base

    seconds = round_result(size_in_bits / rate_in_bps)
    return {"seconds": seconds, "human_readable": _seconds_to_human_readable(seconds)}


def calculate_transfer_time(size_value: float, size_unit: str, rate_value: float, rate_unit: str) -> dict:
    """
    Tempo estimado de transferência local (ex: copiar pra um pendrive):
    tamanho do arquivo (Armazenamento) dividido pela velocidade de
    transferência (Velocidade). Diferente de calculate_download_time,
    aqui as duas tabelas têm dimensões diferentes — bit vs byte/s —
    então o tamanho precisa virar byte antes da divisão.
    """
    validate_non_negative(size_value)
    validate_non_negative(rate_value)

    size_unit_def = get_unit_or_raise(STORAGE_UNITS, size_unit, "armazenamento")
    rate_unit_def = get_unit_or_raise(SPEED_UNITS, rate_unit, "velocidade")

    if rate_value == 0:
        raise InvalidValueError("A velocidade de transferência não pode ser zero — divisão por zero.")

    size_in_bytes = (size_value * size_unit_def.factor_to_base) / 8
    rate_in_bytes_per_second = rate_value * rate_unit_def.factor_to_base

    seconds = round_result(size_in_bytes / rate_in_bytes_per_second)
    return {"seconds": seconds, "human_readable": _seconds_to_human_readable(seconds)}


def calculate_files_that_fit(
    file_size_value: float,
    file_size_unit: str,
    device_capacity_value: float,
    device_capacity_unit: str,
) -> dict:
    """
    Quantos arquivos de um tamanho médio cabem numa capacidade REAL de
    dispositivo (ex: quantas fotos de 5MB cabem num cartão de 32GB
    anunciado, que na prática tem só ~29.8 GiB disponíveis).

    De propósito usa a unidade REAL de Capacidade de Dispositivo, não a
    anunciada — é isso que o usuário realmente tem disponível.
    """
    validate_non_negative(file_size_value)
    validate_non_negative(device_capacity_value)

    file_unit_def = get_unit_or_raise(STORAGE_UNITS, file_size_unit, "armazenamento")
    capacity_unit_def = get_unit_or_raise(
        DEVICE_CAPACITY_REAL_UNITS, device_capacity_unit, "capacidade de dispositivo (real)"
    )

    if file_size_value == 0:
        raise InvalidValueError("O tamanho do arquivo não pode ser zero — divisão por zero.")

    file_size_in_bytes = (file_size_value * file_unit_def.factor_to_base) / 8
    capacity_in_bytes = device_capacity_value * capacity_unit_def.factor_to_base

    files_that_fit = math.floor(capacity_in_bytes / file_size_in_bytes)
    leftover_bytes = round_result(capacity_in_bytes - (files_that_fit * file_size_in_bytes))

    return {
        "files_that_fit": files_that_fit,
        "leftover_bytes": leftover_bytes,
        # reaproveita o proprio storage_service pra mostrar a sobra numa unidade legivel
        "leftover_in_units": convert_storage(leftover_bytes * 8, "bit"),
    }
