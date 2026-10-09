from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class GradeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    grade_id: int = Field(validation_alias="GradeId")
    job_codeasgrade_code: str = Field(validation_alias="JobCodeasgradeCode")
    job_title: str | None = Field(default=None, validation_alias="JobTitle")
    business_title: str | None = Field(default=None, validation_alias="BusinessTitle")
    grade: str | None = Field(default=None, validation_alias="Grade")


# Fields the Grade grid may sort by (server-side).
GradeSortField = Literal[
    "grade_id",
    "job_codeasgrade_code",
    "job_title",
    "business_title",
    "grade",
]
