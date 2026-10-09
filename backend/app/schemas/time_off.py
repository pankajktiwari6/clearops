from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TimeOffCreate(BaseModel):
    """Payload for creating a gold.TimeOff row (primary key is generated)."""

    hrid: str | None = None
    timeoffdate: date | None = None
    time_offtype: str | None = None
    typedaysorhours: str | None = None
    time_data_approved: bool | None = None


class TimeOffUpdate(BaseModel):
    """Partial update of a gold.TimeOff row -- every field optional."""

    hrid: str | None = None
    timeoffdate: date | None = None
    time_offtype: str | None = None
    typedaysorhours: str | None = None
    time_data_approved: bool | None = None


class TimeOffResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    time_off_id: int = Field(validation_alias="TimeOffId")
    hrid: str | None = Field(default=None, validation_alias="HRID")
    timeoffdate: date | None = Field(default=None, validation_alias="TIMEOFFDATE")
    time_offtype: str | None = Field(default=None, validation_alias="TimeOFFTYPE")
    typedaysorhours: str | None = Field(default=None, validation_alias="TYPEDAYSORHOURS")
    time_data_approved: bool | None = Field(default=None, validation_alias="TimeDataApproved")


# Fields the TimeOff grid may sort by (server-side).
TimeOffSortField = Literal[
    "time_off_id",
    "hrid",
    "timeoffdate",
    "time_offtype",
    "typedaysorhours",
    "time_data_approved",
]
