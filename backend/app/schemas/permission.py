from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PermissionCreate(BaseModel):
    """Payload for creating a gold.ClearOps_Permission row (identity key and audit columns are generated)."""

    role_id: int
    page_id: int
    access_id: int
    hrid: str | None = None
    date_time: datetime | None = None


class PermissionUpdate(BaseModel):
    """Partial update of a gold.ClearOps_Permission row -- every field optional."""

    role_id: int | None = None
    page_id: int | None = None
    hrid: str | None = None
    access_id: int | None = None
    date_time: datetime | None = None


class PermissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    permission_id: int = Field(validation_alias="PermissionId")
    role_id: int = Field(validation_alias="RoleId")
    page_id: int = Field(validation_alias="PageId")
    hrid: str | None = Field(default=None, validation_alias="HRID")
    access_id: int = Field(validation_alias="AccessId")
    date_time: datetime | None = Field(default=None, validation_alias="DateTime")


# Fields the Permission grid may sort by (server-side).
PermissionSortField = Literal[
    "permission_id",
    "role_id",
    "page_id",
    "hrid",
    "access_id",
    "date_time",
]
