from __future__ import annotations

from datetime import date
from uuid import UUID
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class HolidayCreate(BaseModel):
    """Payload for creating a gold.ClearOps_Holiday row (identity key and audit columns are generated)."""

    country: str
    holiday_date: date
    comment: str | None = None
    holiday_name: str | None = None
    source_row_hash: bytes | None = None
    pipeline_run_id: UUID | None = None


class HolidayUpdate(BaseModel):
    """Partial update of a gold.ClearOps_Holiday row -- every field optional."""

    country: str | None = None
    holiday_date: date | None = None
    comment: str | None = None
    holiday_name: str | None = None
    source_row_hash: bytes | None = None
    pipeline_run_id: UUID | None = None


class HolidayResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    holiday_id: int = Field(validation_alias="HolidayId")
    country: str = Field(validation_alias="Country")
    holiday_date: date = Field(validation_alias="HolidayDate")
    comment: str | None = Field(default=None, validation_alias="Comment")
    holiday_name: str | None = Field(default=None, validation_alias="HolidayName")
    source_row_hash: bytes | None = Field(default=None, validation_alias="SourceRowHash")
    pipeline_run_id: UUID | None = Field(default=None, validation_alias="PipelineRunId")


# Fields the Holiday grid may sort by (server-side).
HolidaySortField = Literal[
    "holiday_id",
    "country",
    "holiday_date",
    "comment",
    "holiday_name",
    "source_row_hash",
    "pipeline_run_id",
]
