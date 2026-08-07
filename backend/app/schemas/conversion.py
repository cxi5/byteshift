"""
Schemas de request/response para as rotas de conversão.

Um único schema genérico serve as 4 rotas (/convert/storage, /speed,
/network, /device-capacity) porque o gênero já é definido pela URL —
não faz sentido pedir "gênero" de novo no corpo da requisição e correr
o risco de o campo não bater com a rota chamada. O gênero aparece no
RESPONSE, ecoado pelo próprio endpoint, então a informação não se perde.
"""

from pydantic import BaseModel, Field


class ConversionRequest(BaseModel):
    value: float = Field(..., ge=0, description="Valor a ser convertido. Não aceita negativos.")
    from_unit: str = Field(
        ...,
        min_length=1,
        max_length=64,
        description="Chave da unidade de origem (ex: 'gigabyte').",
    )


class ConversionResponse(BaseModel):
    genre: str = Field(..., description="Gênero da conversão (ex: 'storage').")
    from_unit: str = Field(..., description="Unidade de origem informada na requisição.")
    input_value: float = Field(..., description="Valor de entrada informado na requisição.")
    conversions: dict[str, float] = Field(..., description="Valor convertido em cada unidade do gênero.")
