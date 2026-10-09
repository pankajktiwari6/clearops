from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class FXRateCreate(BaseModel):
    """Payload for creating a gold.ClearOps_FXRates row (identity key and audit columns are generated)."""

    source_funding_currency: str
    target_currency: str
    rate: float | None = None
    is_deleted: bool | None = None
    source_system: str | None = None
    is_user_modified: bool | None = None
    status: str | None = None


class FXRateUpdate(BaseModel):
    """Partial update of a gold.ClearOps_FXRates row -- every field optional."""

    source_funding_currency: str | None = None
    target_currency: str | None = None
    rate: float | None = None
    is_deleted: bool | None = None
    source_system: str | None = None
    is_user_modified: bool | None = None
    status: str | None = None


class FXRateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    fx_rate_id: int = Field(validation_alias="FXRateId")
    source_funding_currency: str = Field(validation_alias="SourceFundingCurrency")
    target_currency: str = Field(validation_alias="TargetCurrency")
    rate: float | None = Field(default=None, validation_alias="Rate")
    row_version: bytes | None = Field(default=None, validation_alias="RowVersion")
    is_deleted: bool | None = Field(default=None, validation_alias="IsDeleted")
    source_system: str | None = Field(default=None, validation_alias="SourceSystem")
    is_user_modified: bool | None = Field(default=None, validation_alias="IsUserModified")
    status: str | None = Field(default=None, validation_alias="Status")


# Fields the FXRate grid may sort by (server-side).
FXRateSortField = Literal[
    "fx_rate_id",
    "source_funding_currency",
    "target_currency",
    "rate",
    "is_deleted",
    "source_system",
    "is_user_modified",
    "status",
]
