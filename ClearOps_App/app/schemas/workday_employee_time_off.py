from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class WorkdayEmployeeTimeOffResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    workday_employee_timeoff_id: int = Field(validation_alias="WorkdayEmployeeTimeOffId")
    hrid: str = Field(validation_alias="HRID")
    month: date = Field(validation_alias="Month")
    scheduled_weekly_hours: float | None = Field(default=None, validation_alias="ScheduledWeeklyHours")
    working_days: float | None = Field(default=None, validation_alias="WorkingDays")
    scheduled_hours: float | None = Field(default=None, validation_alias="ScheduledHours")
    public_holiday_hours: float | None = Field(default=None, validation_alias="PublicHolidayHours")
    pto_hours: float | None = Field(default=None, validation_alias="PTOHours")


# Fields the WorkdayEmployeeTimeOff grid may sort by (server-side).
WorkdayEmployeeTimeOffSortField = Literal[
    "workday_employee_timeoff_id",
    "hrid",
    "month",
    "scheduled_weekly_hours",
    "working_days",
    "scheduled_hours",
    "public_holiday_hours",
    "pto_hours",
]
