from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class LOBCreate(BaseModel):
    """Payload for creating a gold.LOB row (primary key is generated)."""

    lob_name: str | None = None
    entity: str | None = None
    status: str | None = None
    line_of_business_gl: str | None = None
    business_unit: str | None = None


class LOBUpdate(BaseModel):
    """Partial update of a gold.LOB row -- every field optional."""

    lob_name: str | None = None
    entity: str | None = None
    status: str | None = None
    line_of_business_gl: str | None = None
    business_unit: str | None = None


class LOBResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    lob_name: str | None = Field(default=None, validation_alias="LOBName")
    entity: str | None = Field(default=None, validation_alias="Entity")
    status: str | None = Field(default=None, validation_alias="Status")
    lob_id: int = Field(validation_alias="LOBId")
    line_of_business_gl: str | None = Field(default=None, validation_alias="LineOfBusinessGl")
    business_unit: str | None = Field(default=None, validation_alias="BusinessUnit")


# Fields the LOB grid may sort by (server-side).
LOBSortField = Literal[
    "lob_name",
    "entity",
    "status",
    "lob_id",
    "line_of_business_gl",
    "business_unit",
]
