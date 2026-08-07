"""
Schemas para as rotas de conversão contextual (Fase 8).

/download-time e /transfer-time compartilham o mesmo formato de
request/response porque a operação é a mesma (tamanho ÷ velocidade =
tempo) — só muda de qual gênero a velocidade vem. /files-fit é
estruturalmente diferente (duas grandezas de armazenamento, resultado
é uma contagem), por isso tem schemas próprios.
"""

from pydantic import BaseModel, Field


class TransferTimeRequest(BaseModel):
    size_value: float = Field(..., ge=0, description="Tamanho do arquivo, não-negativo.")
    size_unit: str = Field(
        ..., min_length=1, max_length=64, description="Unidade de Armazenamento (ex: 'gigabyte')."
    )
    rate_value: float = Field(..., ge=0, description="Velocidade, não-negativa.")
    rate_unit: str = Field(
        ...,
        min_length=1,
        max_length=64,
        description="Unidade de Rede ou Velocidade (ex: 'megabit_per_second').",
    )


class TransferTimeResponse(BaseModel):
    seconds: float = Field(..., description="Tempo estimado, em segundos.")
    human_readable: str = Field(..., description="Tempo formatado, ex: '1min 20s'.")


class FilesFitRequest(BaseModel):
    file_size_value: float = Field(..., ge=0, description="Tamanho médio de um arquivo, não-negativo.")
    file_size_unit: str = Field(..., min_length=1, max_length=64, description="Unidade de Armazenamento.")
    device_capacity_value: float = Field(..., ge=0, description="Capacidade do dispositivo, não-negativa.")
    device_capacity_unit: str = Field(
        ...,
        min_length=1,
        max_length=64,
        description="Unidade REAL de Capacidade de Dispositivo (ex: 'gibibyte').",
    )


class FilesFitResponse(BaseModel):
    files_that_fit: int = Field(..., description="Quantidade inteira de arquivos que cabem.")
    leftover_bytes: float = Field(..., description="Espaço restante, em bytes.")
    leftover_in_units: dict[str, float] = Field(
        ..., description="Espaço restante convertido em todas as unidades de Armazenamento."
    )
