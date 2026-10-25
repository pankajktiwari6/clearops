from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ProjectSTPSettingCreate(BaseModel):
    """Payload for saving an STP query (identity key and audit columns are generated)."""

    user_id: int
    filter_name: str = Field(min_length=1, max_length=200)
    project_ids: list[int] = Field(min_length=1)
    selected_projects: dict[str, Any] | None = None
    date_time: datetime | None = None


class ProjectSTPSettingUpdate(BaseModel):
    """Partial update -- every field optional."""

    user_id: int | None = None
    filter_name: str | None = Field(default=None, min_length=1, max_length=200)
    project_ids: list[int] | None = Field(default=None, min_length=1)
    selected_projects: dict[str, Any] | None = None
    date_time: datetime | None = None


class ProjectSTPSettingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    stp_setting_id: int = Field(validation_alias="STPSettingId")
    user_id: int = Field(validation_alias="UserId")
    filter_name: str = Field(validation_alias="FilterName")
    project_ids: list[int] = Field(validation_alias="ProjectIds")
    selected_projects: dict[str, Any] | None = Field(default=None, validation_alias="SelectedProjects")
    date_time: datetime | None = Field(default=None, validation_alias="DateTime")


ProjectSTPSettingSortField = Literal[
    "stp_setting_id", "user_id", "filter_name", "date_time",
]
