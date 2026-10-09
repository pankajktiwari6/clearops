from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PageCreate(BaseModel):
    """Payload for creating a gold.ClearOps_Page row (identity key and audit columns are generated)."""

    page_name: str
    page_number: int | None = None
    date_time: datetime | None = None


class PageUpdate(BaseModel):
    """Partial update of a gold.ClearOps_Page row -- every field optional."""

    page_number: int | None = None
    page_name: str | None = None
    date_time: datetime | None = None


class PageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    row_id: int = Field(validation_alias="RowId")
    page_number: int | None = Field(default=None, validation_alias="PageNumber")
    page_name: str = Field(validation_alias="PageName")
    date_time: datetime | None = Field(default=None, validation_alias="DateTime")


# Fields the Page grid may sort by (server-side).
PageSortField = Literal[
    "row_id",
    "page_number",
    "page_name",
    "date_time",
]
