from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    """Payload for creating a gold.ClearOps_Users row (identity key and audit columns are generated)."""

    hrid: str
    role_id: int | None = None
    role_name: str | None = None
    name: str | None = None
    email: str | None = None
    module: str | None = None
    date_time: datetime | None = None


class UserUpdate(BaseModel):
    """Partial update of a gold.ClearOps_Users row -- every field optional."""

    hrid: str | None = None
    role_id: int | None = None
    role_name: str | None = None
    name: str | None = None
    email: str | None = None
    module: str | None = None
    date_time: datetime | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    user_id: int = Field(validation_alias="UserID")
    hrid: str = Field(validation_alias="HRID")
    role_id: int | None = Field(default=None, validation_alias="RoleId")
    role_name: str | None = Field(default=None, validation_alias="RoleName")
    name: str | None = Field(default=None, validation_alias="Name")
    email: str | None = Field(default=None, validation_alias="Email")
    module: str | None = Field(default=None, validation_alias="Module")
    date_time: datetime | None = Field(default=None, validation_alias="DateTime")


# Fields the User grid may sort by (server-side).
UserSortField = Literal[
    "user_id",
    "hrid",
    "role_id",
    "role_name",
    "name",
    "email",
    "module",
    "date_time",
]
