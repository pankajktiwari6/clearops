from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ResourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    resource_id: int = Field(validation_alias="ResourceID")
    hrid: str = Field(validation_alias="HRID")
    name: str | None = Field(default=None, validation_alias="Name")
    start_date: date | None = Field(default=None, validation_alias="StartDate")
    end_date: date | None = Field(default=None, validation_alias="EndDate")
    grade_id: int | None = Field(default=None, validation_alias="GradeId")
    email: str | None = Field(default=None, validation_alias="Email")
    lob_id: int | None = Field(default=None, validation_alias="LOBId")
    budget: float | None = Field(default=None, validation_alias="Budget")
    weekly_hours: float | None = Field(default=None, validation_alias="WeeklyHours")
    status: str | None = Field(default=None, validation_alias="Status")


# Fields the Resource grid may sort by (server-side).
ResourceSortField = Literal[
    "resource_id",
    "hrid",
    "name",
    "start_date",
    "end_date",
    "grade_id",
    "email",
    "lob_id",
    "budget",
    "weekly_hours",
    "status",
]
