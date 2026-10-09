from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class LogCreate(BaseModel):
    """Payload for creating a gold.ClearOps_Logs_table row (identity key and audit columns are generated)."""

    sys_integration_id: int | None = None
    cornjob_run_id: str | None = None
    date_time: datetime | None = None


class LogUpdate(BaseModel):
    """Partial update of a gold.ClearOps_Logs_table row -- every field optional."""

    sys_integration_id: int | None = None
    cornjob_run_id: str | None = None
    date_time: datetime | None = None


class LogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    log_id: int = Field(validation_alias="LogId")
    sys_integration_id: int | None = Field(default=None, validation_alias="SysIntegrationId")
    cornjob_run_id: str | None = Field(default=None, validation_alias="CornjobRunId")
    date_time: datetime | None = Field(default=None, validation_alias="DateTime")


# Fields the Log grid may sort by (server-side).
LogSortField = Literal[
    "log_id",
    "sys_integration_id",
    "cornjob_run_id",
    "date_time",
]
