from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class LoginCreate(BaseModel):
    """Payload for creating a clearops.Login row (primary key is generated)."""

    sso: str | None = None
    email: str | None = None
    hrid: str | None = None
    date_time: datetime | None = None


class LoginUpdate(BaseModel):
    """Partial update of a clearops.Login row -- every field optional."""

    sso: str | None = None
    email: str | None = None
    hrid: str | None = None
    date_time: datetime | None = None


class LoginResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    user_login_id: int = Field(validation_alias="UserLoginId")
    sso: str | None = Field(default=None, validation_alias="SSO")
    email: str | None = Field(default=None, validation_alias="Email")
    hrid: str | None = Field(default=None, validation_alias="HRID")
    date_time: datetime | None = Field(default=None, validation_alias="DateTime")


# Fields the Login grid may sort by (server-side).
LoginSortField = Literal[
    "user_login_id",
    "sso",
    "email",
    "hrid",
    "date_time",
]
