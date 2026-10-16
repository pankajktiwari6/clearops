from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class OTLTimecardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    otl_timecard_id: int = Field(validation_alias="OTLTimecardID")
    project_num: str | None = Field(default=None, validation_alias="PROJECTNUM")
    task_number: str | None = Field(default=None, validation_alias="TASKNUMBER")
    time_entry_date: date = Field(validation_alias="TIMEENTRYDATE")
    employee_number: str | None = Field(default=None, validation_alias="EMPLOYEENUMBER")
    task_name: str | None = Field(default=None, validation_alias="TASKNAME")
    hours_type: str | None = Field(default=None, validation_alias="HOURSTYPE")
    hours: float | None = Field(default=None, validation_alias="HOURS")
    status: str | None = Field(default=None, validation_alias="STATUS")
    period: str | None = Field(default=None, validation_alias="PERIOD")
    comments: str | None = Field(default=None, validation_alias="COMMENTS")
    last_update_date: datetime | None = Field(default=None, validation_alias="LastUpdateDate")
    last_processed_date: datetime | None = Field(default=None, validation_alias="LastProcessedDate")
    dl_last_processed_date: datetime | None = Field(default=None, validation_alias="DlLastProcessedDate")
    sourcemodifieddate: datetime | None = Field(default=None, validation_alias="SourceModifiedDate")
    loadbatchid: str | None = Field(default=None, validation_alias="LoadBatchId")
    stageinsertedtimestamp: datetime | None = Field(default=None, validation_alias="StageInsertedTimestamp")
    isprocessed: bool | None = Field(default=None, validation_alias="IsProcessed")


# Fields the OTLTimecard grid may sort by (server-side).
OTLTimecardSortField = Literal[
    "otl_timecard_id",
    "project_num",
    "task_number",
    "time_entry_date",
    "employee_number",
    "task_name",
    "hours_type",
    "hours",
    "status",
    "period",
    "comments",
    "last_update_date",
    "last_processed_date",
    "dl_last_processed_date",
    "sourcemodifieddate",
    "loadbatchid",
    "stageinsertedtimestamp",
    "isprocessed",
]
