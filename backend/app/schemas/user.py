from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    """Payload for creating a clearops.User row (primary key is generated)."""

    hrid: str | None = None
    role_id: int | None = None
    role_name: str | None = None
    name: str | None = None
    email: str | None = None
    module: str | None = None
    date_time: datetime | None = None


class UserUpdate(BaseModel):
    """Partial update of a clearops.User row -- every field optional."""

    hrid: str | None = None
    role_id: int | None = None
    role_name: str | None = None
    name: str | None = None
    email: str | None = None
    module: str | None = None
    date_time: datetime | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    hrid: str | None = Field(default=None, validation_alias="HRID")
    role_id: int | None = Field(default=None, validation_alias="RoleId")
    role_name: str | None = Field(default=None, validation_alias="RoleName")
    name: str | None = Field(default=None, validation_alias="Name")
    email: str | None = Field(default=None, validation_alias="Email")
    user_id: int = Field(validation_alias="UserID")
    module: str | None = Field(default=None, validation_alias="Module")
    date_time: datetime | None = Field(default=None, validation_alias="DateTime")


# Fields the User grid may sort by (server-side).
UserSortField = Literal[
    "hrid",
    "role_id",
    "role_name",
    "name",
    "email",
    "user_id",
    "module",
    "date_time",
]
