from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class RoleCreate(BaseModel):
    """Payload for creating a gold.Role row (primary key is generated)."""

    role_name: str | None = None
    role_type: str | None = None


class RoleUpdate(BaseModel):
    """Partial update of a gold.Role row -- every field optional."""

    role_name: str | None = None
    role_type: str | None = None


class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    role_name: str | None = Field(default=None, validation_alias="RoleName")
    role_type: str | None = Field(default=None, validation_alias="RoleType")
    role_id: int = Field(validation_alias="RoleId")


# Fields the Role grid may sort by (server-side).
RoleSortField = Literal[
    "role_name",
    "role_type",
    "role_id",
]
