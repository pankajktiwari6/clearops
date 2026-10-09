from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AccessCreate(BaseModel):
    """Payload for creating a gold.ClearOps_Access_table row (identity key and audit columns are generated)."""

    accrss_type: str
    date_time: datetime | None = None


class AccessUpdate(BaseModel):
    """Partial update of a gold.ClearOps_Access_table row -- every field optional."""

    accrss_type: str | None = None
    date_time: datetime | None = None


class AccessResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    access_id: int = Field(validation_alias="AccessID")
    accrss_type: str = Field(validation_alias="AccrssType")
    date_time: datetime | None = Field(default=None, validation_alias="DateTime")


# Fields the Access grid may sort by (server-side).
AccessSortField = Literal[
    "access_id",
    "accrss_type",
    "date_time",
]
