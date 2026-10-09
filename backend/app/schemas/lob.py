from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class LOBResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    lob_id: int = Field(validation_alias="LOBId")
    lob_name: str = Field(validation_alias="LOBName")
    entity: str | None = Field(default=None, validation_alias="Entity")
    status: str | None = Field(default=None, validation_alias="Status")
    line_of_business_gl: str | None = Field(default=None, validation_alias="LineOfBusinessGl")
    business_unit: str | None = Field(default=None, validation_alias="BusinessUnit")


# Fields the LOB grid may sort by (server-side).
LOBSortField = Literal[
    "lob_id",
    "lob_name",
    "entity",
    "status",
    "line_of_business_gl",
    "business_unit",
]
