from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class LogCreate(BaseModel):
    """Payload for creating a gold.Log row (primary key is generated)."""

    sys_integration_id: int | None = None
    cornjobrun_id: int | None = None
    date_time: datetime | None = None


class LogUpdate(BaseModel):
    """Partial update of a gold.Log row -- every field optional."""

    sys_integration_id: int | None = None
    cornjobrun_id: int | None = None
    date_time: datetime | None = None


class LogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    log_id: int = Field(validation_alias="LogId")
    sys_integration_id: int | None = Field(default=None, validation_alias="SysIntegrationId")
    cornjobrun_id: int | None = Field(default=None, validation_alias="CornjobrunId")
    date_time: datetime | None = Field(default=None, validation_alias="DateTime")


# Fields the Log grid may sort by (server-side).
LogSortField = Literal[
    "log_id",
    "sys_integration_id",
    "cornjobrun_id",
    "date_time",
]
