from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ProjectWBSCreate(BaseModel):
    """Payload for creating a gold.ProjectWBS row (primary key is generated)."""

    task_id: int | None = None
    parent_task_id: int | None = None
    wbs_level: str | None = None
    task_type: str | None = None
    task_name: str | None = None
    task_number: str | None = None
    delivery_type: str | None = None
    task_start_date: date | None = None
    task_end_date: date | None = None
    chargeable_flag: bool | None = None
    billable_flag: bool | None = None
    current_budget_revenue: float | None = None
    current_budget_cost: float | None = None
    itd_actuals: float | None = None
    project_id: int | None = None
    top_task_id: int | None = None
    created_by: str | None = None
    created_date: datetime | None = None
    modified_by: str | None = None
    modified_date: datetime | None = None
    pbu: str | None = None
    service_type_code: str | None = None
    upc: str | None = None
    period_name: str | None = None


class ProjectWBSUpdate(BaseModel):
    """Partial update of a gold.ProjectWBS row -- every field optional."""

    task_id: int | None = None
    parent_task_id: int | None = None
    wbs_level: str | None = None
    task_type: str | None = None
    task_name: str | None = None
    task_number: str | None = None
    delivery_type: str | None = None
    task_start_date: date | None = None
    task_end_date: date | None = None
    chargeable_flag: bool | None = None
    billable_flag: bool | None = None
    current_budget_revenue: float | None = None
    current_budget_cost: float | None = None
    itd_actuals: float | None = None
    project_id: int | None = None
    top_task_id: int | None = None
    created_by: str | None = None
    created_date: datetime | None = None
    modified_by: str | None = None
    modified_date: datetime | None = None
    pbu: str | None = None
    service_type_code: str | None = None
    upc: str | None = None
    period_name: str | None = None


class ProjectWBSResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    task_id: int | None = Field(default=None, validation_alias="TaskId")
    parent_task_id: int | None = Field(default=None, validation_alias="ParentTaskID")
    wbs_level: str | None = Field(default=None, validation_alias="WBSLevel")
    task_type: str | None = Field(default=None, validation_alias="TaskType")
    task_name: str | None = Field(default=None, validation_alias="TaskName")
    task_number: str | None = Field(default=None, validation_alias="TaskNumber")
    delivery_type: str | None = Field(default=None, validation_alias="DeliveryType")
    task_start_date: date | None = Field(default=None, validation_alias="TaskStartDate")
    task_end_date: date | None = Field(default=None, validation_alias="TaskEndDate")
    chargeable_flag: bool | None = Field(default=None, validation_alias="ChargeableFlag")
    billable_flag: bool | None = Field(default=None, validation_alias="BillableFlag")
    current_budget_revenue: float | None = Field(default=None, validation_alias="CurrentBudgetRevenue")
    current_budget_cost: float | None = Field(default=None, validation_alias="CurrentBudgetCost")
    itd_actuals: float | None = Field(default=None, validation_alias="ITDActuals")
    project_id: int | None = Field(default=None, validation_alias="ProjectId")
    top_task_id: int | None = Field(default=None, validation_alias="TopTaskId")
    project_wbs_id: int = Field(validation_alias="ProjectWBSId")
    created_by: str | None = Field(default=None, validation_alias="CreatedBy")
    created_date: datetime | None = Field(default=None, validation_alias="CreatedDate")
    modified_by: str | None = Field(default=None, validation_alias="ModifiedBy")
    modified_date: datetime | None = Field(default=None, validation_alias="ModifiedDate")
    pbu: str | None = Field(default=None, validation_alias="PBU")
    service_type_code: str | None = Field(default=None, validation_alias="ServiceTypeCode")
    upc: str | None = Field(default=None, validation_alias="UPC")
    period_name: str | None = Field(default=None, validation_alias="PeriodName")


# Fields the ProjectWBS grid may sort by (server-side).
ProjectWBSSortField = Literal[
    "task_id",
    "parent_task_id",
    "wbs_level",
    "task_type",
    "task_name",
    "task_number",
    "delivery_type",
    "task_start_date",
    "task_end_date",
    "chargeable_flag",
    "billable_flag",
    "current_budget_revenue",
    "current_budget_cost",
    "itd_actuals",
    "project_id",
    "top_task_id",
    "project_wbs_id",
    "created_by",
    "created_date",
    "modified_by",
    "modified_date",
    "pbu",
    "service_type_code",
    "upc",
    "period_name",
]
