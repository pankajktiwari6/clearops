from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AdminIntegrationStatusCreate(BaseModel):
    """Payload for creating a gold.AdminIntegrationStatus row (primary key is generated)."""

    system: str | None = None
    last_sync: datetime | None = None
    status: str | None = None
    record_captured: str | None = None
    date_time: datetime | None = None


class AdminIntegrationStatusUpdate(BaseModel):
    """Partial update of a gold.AdminIntegrationStatus row -- every field optional."""

    system: str | None = None
    last_sync: datetime | None = None
    status: str | None = None
    record_captured: str | None = None
    date_time: datetime | None = None


class AdminIntegrationStatusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    system: str | None = Field(default=None, validation_alias="System")
    last_sync: datetime | None = Field(default=None, validation_alias="LastSync")
    status: str | None = Field(default=None, validation_alias="Status")
    record_captured: str | None = Field(default=None, validation_alias="RecordCaptured")
    sys_integration_id: int = Field(validation_alias="SysIntegrationId")
    date_time: datetime | None = Field(default=None, validation_alias="DateTime")


# Fields the AdminIntegrationStatus grid may sort by (server-side).
AdminIntegrationStatusSortField = Literal[
    "system",
    "last_sync",
    "status",
    "record_captured",
    "sys_integration_id",
    "date_time",
]
