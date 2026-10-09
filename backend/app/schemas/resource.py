from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ResourceCreate(BaseModel):
    """Payload for creating a clearops.Resource row (primary key is generated)."""

    hrid: str | None = None
    name: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    grade_id: int | None = None
    email: str | None = None
    lob_id: int | None = None
    budget: float | None = None
    weekly_hours: float | None = None
    status: str | None = None


class ResourceUpdate(BaseModel):
    """Partial update of a clearops.Resource row -- every field optional."""

    hrid: str | None = None
    name: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    grade_id: int | None = None
    email: str | None = None
    lob_id: int | None = None
    budget: float | None = None
    weekly_hours: float | None = None
    status: str | None = None


class ResourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    hrid: str | None = Field(default=None, validation_alias="HRID")
    name: str | None = Field(default=None, validation_alias="Name")
    start_date: date | None = Field(default=None, validation_alias="StartDate")
    end_date: date | None = Field(default=None, validation_alias="EndDate")
    grade_id: int | None = Field(default=None, validation_alias="GradeId")
    email: str | None = Field(default=None, validation_alias="Email")
    lob_id: int | None = Field(default=None, validation_alias="LOBId")
    budget: float | None = Field(default=None, validation_alias="Budget")
    resource_id: int = Field(validation_alias="ResourceID")
    weekly_hours: float | None = Field(default=None, validation_alias="WeeklyHours")
    status: str | None = Field(default=None, validation_alias="Status")


# Fields the Resource grid may sort by (server-side).
ResourceSortField = Literal[
    "hrid",
    "name",
    "start_date",
    "end_date",
    "grade_id",
    "email",
    "lob_id",
    "budget",
    "resource_id",
    "weekly_hours",
    "status",
]
