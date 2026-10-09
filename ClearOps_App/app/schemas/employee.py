from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    row_id: int = Field(validation_alias="RowId")
    hrid: str = Field(validation_alias="HRID")
    preferred_first_name: str | None = Field(default=None, validation_alias="PreferredFirstName")
    last_name: str | None = Field(default=None, validation_alias="LastName")
    continuous_service_date: date | None = Field(default=None, validation_alias="ContinuousServiceDate")
    first_start_date: date | None = Field(default=None, validation_alias="FirstStartDate")
    last_start_date: date | None = Field(default=None, validation_alias="LastStartDate")
    expected_end_date: str | None = Field(default=None, validation_alias="ExpectedEndDate")
    job_code: str | None = Field(default=None, validation_alias="JobCode")
    job_title: str | None = Field(default=None, validation_alias="JobTitle")
    business_title: str | None = Field(default=None, validation_alias="BusinessTitle")
    grade_id: int | None = Field(default=None, validation_alias="GradeID")
    job_entry_date: date | None = Field(default=None, validation_alias="JobEntryDate")
    line_of_business: str | None = Field(default=None, validation_alias="LineOfBusiness")
    line_of_business_code: str | None = Field(default=None, validation_alias="LineOfBusinessCode")
    country: str | None = Field(default=None, validation_alias="Country")
    reg_temp: str | None = Field(default=None, validation_alias="RegTemp")
    full_part: str | None = Field(default=None, validation_alias="FullPart")
    fte: float | None = Field(default=None, validation_alias="FTE")
    region: str | None = Field(default=None, validation_alias="Region")
    email: str | None = Field(default=None, validation_alias="Email")
    scheduled_weekly_hours: float | None = Field(default=None, validation_alias="ScheduledWeeklyHours")
    row_version: bytes | None = Field(default=None, validation_alias="RowVersion")
    is_deleted: bool | None = Field(default=None, validation_alias="IsDeleted")
    source_system: str | None = Field(default=None, validation_alias="SourceSystem")
    is_user_modified: bool | None = Field(default=None, validation_alias="IsUserModified")
    lobid: int | None = Field(default=None, validation_alias="LOBID")
    project_id: int | None = Field(default=None, validation_alias="ProjectId")


# Fields the Employee grid may sort by (server-side).
EmployeeSortField = Literal[
    "row_id",
    "hrid",
    "preferred_first_name",
    "last_name",
    "continuous_service_date",
    "first_start_date",
    "last_start_date",
    "expected_end_date",
    "job_code",
    "job_title",
    "business_title",
    "grade_id",
    "job_entry_date",
    "line_of_business",
    "line_of_business_code",
    "country",
    "reg_temp",
    "full_part",
    "fte",
    "region",
    "email",
    "scheduled_weekly_hours",
    "is_deleted",
    "source_system",
    "is_user_modified",
    "lobid",
    "project_id",
]
