from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ProjectWBSResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    project_wbs_id: int = Field(validation_alias="ProjectWBSId")
    task_id: str | None = Field(default=None, validation_alias="TaskId")
    parent_task_id: str | None = Field(default=None, validation_alias="ParentTaskID")
    wbs_level: str | None = Field(default=None, validation_alias="WBSLevel")
    task_type: str | None = Field(default=None, validation_alias="TaskType")
    task_name: str | None = Field(default=None, validation_alias="TaskName")
    task_number: str = Field(validation_alias="TaskNumber")
    delivery_type: str | None = Field(default=None, validation_alias="DeliveryType")
    task_start_date: datetime | None = Field(default=None, validation_alias="TaskStartDate")
    task_end_date: datetime | None = Field(default=None, validation_alias="TaskEndDate")
    chargeable_flag: bool | None = Field(default=None, validation_alias="ChargeableFlag")
    billable_flag: bool | None = Field(default=None, validation_alias="BillableFlag")
    current_budget_revenue_by_task: float | None = Field(default=None, validation_alias="CurrentBudgetRevenueByTask")
    current_budget_cost_by_task: float | None = Field(default=None, validation_alias="CurrentBudgetCostByTask")
    itd_actuals_hours: float | None = Field(default=None, validation_alias="ITDActualsHours")
    project_id: int = Field(validation_alias="ProjectId")
    top_task_id: str | None = Field(default=None, validation_alias="TopTaskId")
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
    "project_wbs_id",
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
    "current_budget_revenue_by_task",
    "current_budget_cost_by_task",
    "itd_actuals_hours",
    "project_id",
    "top_task_id",
    "created_by",
    "created_date",
    "modified_by",
    "modified_date",
    "pbu",
    "service_type_code",
    "upc",
    "period_name",
]
