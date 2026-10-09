from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TimeOffResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    time_off_id: int = Field(validation_alias="TimeOffId")
    hrid: str = Field(validation_alias="HRID")
    timeoffdate: date = Field(validation_alias="TIMEOFFDATE")
    time_offtype: str | None = Field(default=None, validation_alias="TimeOFFTYPE")
    typedaysorhours: str | None = Field(default=None, validation_alias="TYPEDAYSORHOURS")
    time_data_approved: date | None = Field(default=None, validation_alias="TimeDataApproved")


# Fields the TimeOff grid may sort by (server-side).
TimeOffSortField = Literal[
    "time_off_id",
    "hrid",
    "timeoffdate",
    "time_offtype",
    "typedaysorhours",
    "time_data_approved",
]
