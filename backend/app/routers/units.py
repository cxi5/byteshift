"""
Rota /units — lista as unidades disponíveis por gênero.
O frontend usa isso pra montar os cards dinamicamente, sem hardcode.
"""

from fastapi import APIRouter

from app.core.constants import (
    DEVICE_CAPACITY_ADVERTISED_UNITS,
    DEVICE_CAPACITY_REAL_UNITS,
    NETWORK_UNITS,
    SPEED_UNITS,
    STORAGE_UNITS,
)
from app.schemas.units import GenreUnits, UnitInfo

router = APIRouter(prefix="/units", tags=["units"])


def _to_unit_info(units_table: dict) -> list[UnitInfo]:
    return [
        UnitInfo(key=u.key, symbol=u.symbol, label=u.label, system=u.system)
        for u in units_table.values()
    ]


@router.get("", response_model=list[GenreUnits])
def list_units() -> list[GenreUnits]:
    return [
        GenreUnits(genre="storage", units=_to_unit_info(STORAGE_UNITS)),
        GenreUnits(genre="speed", units=_to_unit_info(SPEED_UNITS)),
        GenreUnits(genre="network", units=_to_unit_info(NETWORK_UNITS)),
        GenreUnits(
            genre="device-capacity-advertised",
            units=_to_unit_info(DEVICE_CAPACITY_ADVERTISED_UNITS),
        ),
        GenreUnits(
            genre="device-capacity-real",
            units=_to_unit_info(DEVICE_CAPACITY_REAL_UNITS),
        ),
    ]
