from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class RoleCreate(BaseModel):
    """Payload for creating a gold.ClearOps_Role row (identity key and audit columns are generated)."""

    role_name: str
    role_type: str | None = None


class RoleUpdate(BaseModel):
    """Partial update of a gold.ClearOps_Role row -- every field optional."""

    role_name: str | None = None
    role_type: str | None = None


class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    role_id: int = Field(validation_alias="RoleId")
    role_name: str = Field(validation_alias="RoleName")
    role_type: str | None = Field(default=None, validation_alias="RoleType")


# Fields the Role grid may sort by (server-side).
RoleSortField = Literal[
    "role_id",
    "role_name",
    "role_type",
]
