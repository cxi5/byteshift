"""
Rotas de conversão — uma por gênero, cada uma delegando pro serviço
isolado correspondente. Erros de negócio (unidade inválida, valor
inválido) viram HTTP 422 com mensagem clara, nunca um resultado
silencioso ou fictício.
"""

from fastapi import APIRouter, HTTPException

from app.core.exceptions import ConversionError
from app.schemas.conversion import ConversionRequest, ConversionResponse
from app.services.device_capacity_service import convert_device_capacity
from app.services.network_service import convert_network
from app.services.speed_service import convert_speed
from app.services.storage_service import convert_storage

router = APIRouter(prefix="/convert", tags=["convert"])


def _convert_and_respond(genre: str, payload: ConversionRequest, convert_fn) -> ConversionResponse:
    """
    Chama o serviço de conversão do gênero e monta o response padrão.

    Centraliza o try/except que antes se repetia em cada rota. Captura
    ConversionError (classe-base de InvalidUnitError, InvalidValueError
    e NegativeValueError) — não importa qual erro de negócio aconteceu,
    o tratamento é o mesmo: HTTP 422 com a mensagem original.
    """
    try:
        conversions = convert_fn(payload.value, payload.from_unit)
    except ConversionError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e

    return ConversionResponse(
        genre=genre,
        from_unit=payload.from_unit,
        input_value=payload.value,
        conversions=conversions,
    )


@router.post("/storage", response_model=ConversionResponse)
def convert_storage_endpoint(payload: ConversionRequest) -> ConversionResponse:
    return _convert_and_respond("storage", payload, convert_storage)


@router.post("/speed", response_model=ConversionResponse)
def convert_speed_endpoint(payload: ConversionRequest) -> ConversionResponse:
    return _convert_and_respond("speed", payload, convert_speed)


@router.post("/network", response_model=ConversionResponse)
def convert_network_endpoint(payload: ConversionRequest) -> ConversionResponse:
    return _convert_and_respond("network", payload, convert_network)


@router.post("/device-capacity", response_model=ConversionResponse)
def convert_device_capacity_endpoint(payload: ConversionRequest) -> ConversionResponse:
    return _convert_and_respond("device-capacity", payload, convert_device_capacity)
