"""
Schemas para a rota /units — lista as unidades disponíveis por gênero,
usada pelo frontend para montar os cards dinamicamente.
"""

from pydantic import BaseModel

from app.core.constants import UnitSystem


class UnitInfo(BaseModel):
    key: str
    symbol: str
    label: str
    system: UnitSystem  # reaproveita o mesmo tipo de constants.py, evita duas fontes de verdade


class GenreUnits(BaseModel):
    genre: str
    units: list[UnitInfo]
