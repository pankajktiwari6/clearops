from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EstimatorVersionCreate(BaseModel):
    """Payload for saving a new estimate version (version number, active flag and audit columns are generated)."""

    project_id: str
    change_summary: str | None = Field(default=None, max_length=500)
    line_count: int = 0
    total: float | None = None
    snapshot: str  # JSON text of the estimate lines


class EstimatorVersionSummary(BaseModel):
    """Row of the version picker -- no snapshot, so the list stays light."""

    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    version_id: int = Field(validation_alias="VersionId")
    project_id: str = Field(validation_alias="ProjectId")
    version_no: int = Field(validation_alias="VersionNo")
    change_summary: str | None = Field(default=None, validation_alias="Summary")
    line_count: int = Field(default=0, validation_alias="LineCount")
    total: float | None = Field(default=None, validation_alias="Total")
    is_active: bool = Field(default=False, validation_alias="IsActive")
    activated_by: str | None = Field(default=None, validation_alias="ActivatedBy")
    activated_date: datetime | None = Field(default=None, validation_alias="ActivatedDate")
    created_by: str | None = Field(default=None, validation_alias="GoldCreatedBy")
    created_date: datetime | None = Field(default=None, validation_alias="GoldCreatedDate")


class EstimatorVersionResponse(EstimatorVersionSummary):
    """A single version including its full snapshot."""

    snapshot: str = Field(validation_alias="Snapshot")


class EstimatorTemplateCreate(BaseModel):
    """Payload for creating a template (id and audit columns are generated)."""

    name: str = Field(max_length=200)
    source_project_id: str | None = Field(default=None, max_length=100)
    task_count: int = 0
    content: str  # JSON text of roles per task


class EstimatorTemplateUpdate(BaseModel):
    """Partial update of a template -- every field optional."""

    name: str | None = Field(default=None, max_length=200)
    source_project_id: str | None = Field(default=None, max_length=100)
    task_count: int | None = None
    content: str | None = None


class EstimatorTemplateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    template_id: int = Field(validation_alias="TemplateId")
    name: str = Field(validation_alias="Name")
    source_project_id: str | None = Field(default=None, validation_alias="SourceProjectId")
    task_count: int = Field(default=0, validation_alias="TaskCount")
    content: str = Field(validation_alias="Content")
    created_by: str | None = Field(default=None, validation_alias="GoldCreatedBy")
    created_date: datetime | None = Field(default=None, validation_alias="GoldCreatedDate")
