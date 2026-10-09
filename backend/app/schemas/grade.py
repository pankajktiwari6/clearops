from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class GradeCreate(BaseModel):
    """Payload for creating a gold.Grade row (primary key is generated)."""

    job_code: str | None = None
    job_title: str | None = None
    business_title: str | None = None
    grade: str | None = None


class GradeUpdate(BaseModel):
    """Partial update of a gold.Grade row -- every field optional."""

    job_code: str | None = None
    job_title: str | None = None
    business_title: str | None = None
    grade: str | None = None


class GradeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    job_code: str | None = Field(default=None, validation_alias="JobCode")
    job_title: str | None = Field(default=None, validation_alias="JobTitle")
    business_title: str | None = Field(default=None, validation_alias="BusinessTitle")
    grade_id: int = Field(validation_alias="GradeId")
    grade: str | None = Field(default=None, validation_alias="Grade")


# Fields the Grade grid may sort by (server-side).
GradeSortField = Literal[
    "job_code",
    "job_title",
    "business_title",
    "grade_id",
    "grade",
]
