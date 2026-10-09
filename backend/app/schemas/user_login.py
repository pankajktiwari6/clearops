from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class UserLoginCreate(BaseModel):
    """Payload for creating a gold.UserLogin row (primary key is generated)."""

    email: str | None = None
    logindatetimestampe: datetime | None = None
    status: str | None = None
    date_time: datetime | None = None


class UserLoginUpdate(BaseModel):
    """Partial update of a gold.UserLogin row -- every field optional."""

    email: str | None = None
    logindatetimestampe: datetime | None = None
    status: str | None = None
    date_time: datetime | None = None


class UserLoginResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    userid: int = Field(validation_alias="Userid")
    email: str | None = Field(default=None, validation_alias="Email")
    logindatetimestampe: datetime | None = Field(default=None, validation_alias="Logindatetimestampe")
    status: str | None = Field(default=None, validation_alias="Status")
    date_time: datetime | None = Field(default=None, validation_alias="DateTime")


# Fields the UserLogin grid may sort by (server-side).
UserLoginSortField = Literal[
    "userid",
    "email",
    "logindatetimestampe",
    "status",
    "date_time",
]
