"""
Rotas de conversão contextual (Fase 8) — combinam dois gêneros numa
única resposta, diferente de /convert/*, que fica dentro de um gênero
só. Ficam sob prefixo próprio (/convert/context) de propósito, pra não
se misturar visualmente nem semanticamente com a conversão direta.
"""

from fastapi import APIRouter, HTTPException

from app.core.exceptions import ConversionError
from app.schemas.context import FilesFitRequest, FilesFitResponse, TransferTimeRequest, TransferTimeResponse
from app.services.context_service import (
    calculate_download_time,
    calculate_files_that_fit,
    calculate_transfer_time,
)

router = APIRouter(prefix="/convert/context", tags=["context"])


@router.post("/download-time", response_model=TransferTimeResponse)
def download_time_endpoint(payload: TransferTimeRequest) -> TransferTimeResponse:
    try:
        result = calculate_download_time(
            payload.size_value, payload.size_unit, payload.rate_value, payload.rate_unit
        )
    except ConversionError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    return TransferTimeResponse(**result)


@router.post("/transfer-time", response_model=TransferTimeResponse)
def transfer_time_endpoint(payload: TransferTimeRequest) -> TransferTimeResponse:
    try:
        result = calculate_transfer_time(
            payload.size_value, payload.size_unit, payload.rate_value, payload.rate_unit
        )
    except ConversionError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    return TransferTimeResponse(**result)


@router.post("/files-fit", response_model=FilesFitResponse)
def files_fit_endpoint(payload: FilesFitRequest) -> FilesFitResponse:
    try:
        result = calculate_files_that_fit(
            payload.file_size_value,
            payload.file_size_unit,
            payload.device_capacity_value,
            payload.device_capacity_unit,
        )
    except ConversionError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    return FilesFitResponse(**result)
