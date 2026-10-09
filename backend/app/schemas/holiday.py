from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class HolidayCreate(BaseModel):
    """Payload for creating a gold.Holiday row (primary key is generated)."""

    country: str | None = None
    holiday_date: date | None = None
    comment: str | None = None
    holiday_name: str | None = None


class HolidayUpdate(BaseModel):
    """Partial update of a gold.Holiday row -- every field optional."""

    country: str | None = None
    holiday_date: date | None = None
    comment: str | None = None
    holiday_name: str | None = None


class HolidayResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    country: str | None = Field(default=None, validation_alias="Country")
    holiday_date: date | None = Field(default=None, validation_alias="HolidayDate")
    comment: str | None = Field(default=None, validation_alias="Comment")
    holiday_id: int = Field(validation_alias="HolidayId")
    holiday_name: str | None = Field(default=None, validation_alias="HolidayName")


# Fields the Holiday grid may sort by (server-side).
HolidaySortField = Literal[
    "country",
    "holiday_date",
    "comment",
    "holiday_id",
    "holiday_name",
]
