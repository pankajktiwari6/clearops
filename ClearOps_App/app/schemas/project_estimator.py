from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ProjectEstimatorCreate(BaseModel):
    """Payload for creating a gold.ProjectEstimator row (identity key and audit columns are generated)."""

    task_id: int | None = None
    job_title: str | None = None
    task_name: str | None = None
    qty: float | None = None
    hrs: float | None = None
    rate: float | None = None
    total: float | None = None
    sub_total: float | None = None
    task_number: str | None = None
    project_id: int | None = None
    parent_task_id: int | None = None
    delivery_type: str | None = None
    resource_id: int | None = None


class ProjectEstimatorUpdate(BaseModel):
    """Partial update of a gold.ProjectEstimator row -- every field optional."""

    task_id: int | None = None
    job_title: str | None = None
    task_name: str | None = None
    qty: float | None = None
    hrs: float | None = None
    rate: float | None = None
    total: float | None = None
    sub_total: float | None = None
    task_number: str | None = None
    project_id: int | None = None
    parent_task_id: int | None = None
    delivery_type: str | None = None
    resource_id: int | None = None


class ProjectEstimatorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    project_estimater_id: int = Field(validation_alias="ProjectEstimaterId")
    task_id: int | None = Field(default=None, validation_alias="TaskID")
    job_title: str | None = Field(default=None, validation_alias="JobTitle")
    task_name: str | None = Field(default=None, validation_alias="TaskName")
    qty: float | None = Field(default=None, validation_alias="QTY")
    hrs: float | None = Field(default=None, validation_alias="HRS")
    rate: float | None = Field(default=None, validation_alias="Rate")
    total: float | None = Field(default=None, validation_alias="Total")
    sub_total: float | None = Field(default=None, validation_alias="SubTotal")
    task_number: str | None = Field(default=None, validation_alias="TaskNumber")
    project_id: int | None = Field(default=None, validation_alias="ProjectId")
    parent_task_id: int | None = Field(default=None, validation_alias="ParentTaskID")
    delivery_type: str | None = Field(default=None, validation_alias="DeliveryType")
    resource_id: int | None = Field(default=None, validation_alias="ResourceId")


# Fields the ProjectEstimator grid may sort by (server-side).
ProjectEstimatorSortField = Literal[
    "project_estimater_id",
    "task_id",
    "job_title",
    "task_name",
    "qty",
    "hrs",
    "rate",
    "total",
    "sub_total",
    "task_number",
    "project_id",
    "parent_task_id",
    "delivery_type",
    "resource_id",
]
