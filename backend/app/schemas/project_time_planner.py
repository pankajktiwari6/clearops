from __future__ import annotations

from datetime import date, time
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ProjectTimePlannerCreate(BaseModel):
    """Payload for creating a clearops.ProjectTimePlanner row (primary key is generated)."""

    task_id: int | None = None
    resource_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    start_time: time | None = None
    end_time: time | None = None
    plan_hours: float | None = None
    description: str | None = None
    completed_status: float | None = None
    is_active: bool | None = None


class ProjectTimePlannerUpdate(BaseModel):
    """Partial update of a clearops.ProjectTimePlanner row -- every field optional."""

    task_id: int | None = None
    resource_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    start_time: time | None = None
    end_time: time | None = None
    plan_hours: float | None = None
    description: str | None = None
    completed_status: float | None = None
    is_active: bool | None = None


class ProjectTimePlannerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    project_time_panner_id: int = Field(validation_alias="ProjectTimePannerId")
    task_id: int | None = Field(default=None, validation_alias="TaskID")
    resource_id: int | None = Field(default=None, validation_alias="ResourceId")
    start_date: date | None = Field(default=None, validation_alias="StartDate")
    end_date: date | None = Field(default=None, validation_alias="EndDate")
    start_time: time | None = Field(default=None, validation_alias="StartTime")
    end_time: time | None = Field(default=None, validation_alias="EndTime")
    plan_hours: float | None = Field(default=None, validation_alias="PlanHours")
    description: str | None = Field(default=None, validation_alias="Description")
    completed_status: float | None = Field(default=None, validation_alias="CompletedStatus")
    is_active: bool | None = Field(default=None, validation_alias="IsActive")


# Fields the ProjectTimePlanner grid may sort by (server-side).
ProjectTimePlannerSortField = Literal[
    "project_time_panner_id",
    "task_id",
    "resource_id",
    "start_date",
    "end_date",
    "start_time",
    "end_time",
    "plan_hours",
    "description",
    "completed_status",
    "is_active",
]
