from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ProjectSTPCreate(BaseModel):
    """Payload for creating a clearops.ProjectSTP row (primary key is generated)."""

    resorce_id: int | None = None
    rate_card_id: int | None = None
    task_start_date: date | None = None
    monthly_value: float | None = None
    monthly_hours: float | None = None
    task_id: int | None = None
    year_months: str | None = None
    date_time: datetime | None = None


class ProjectSTPUpdate(BaseModel):
    """Partial update of a clearops.ProjectSTP row -- every field optional."""

    resorce_id: int | None = None
    rate_card_id: int | None = None
    task_start_date: date | None = None
    monthly_value: float | None = None
    monthly_hours: float | None = None
    task_id: int | None = None
    year_months: str | None = None
    date_time: datetime | None = None


class ProjectSTPResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    resorce_id: int | None = Field(default=None, validation_alias="ResorceId")
    rate_card_id: int | None = Field(default=None, validation_alias="RateCardId")
    task_start_date: date | None = Field(default=None, validation_alias="TaskStartDate")
    monthly_value: float | None = Field(default=None, validation_alias="MonthlyValue")
    monthly_hours: float | None = Field(default=None, validation_alias="MonthlyHours")
    task_id: int | None = Field(default=None, validation_alias="TaskId")
    year_months: str | None = Field(default=None, validation_alias="YearMonths")
    project_stp_id: int = Field(validation_alias="ProjectSTPId")
    date_time: datetime | None = Field(default=None, validation_alias="DateTime")


# Fields the ProjectSTP grid may sort by (server-side).
ProjectSTPSortField = Literal[
    "resorce_id",
    "rate_card_id",
    "task_start_date",
    "monthly_value",
    "monthly_hours",
    "task_id",
    "year_months",
    "project_stp_id",
    "date_time",
]
