from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class FXRateCreate(BaseModel):
    """Payload for creating a gold.FXRate row (primary key is generated)."""

    source_funding_currency: str | None = None
    target_currency: str | None = None
    rate: float | None = None
    status: str | None = None


class FXRateUpdate(BaseModel):
    """Partial update of a gold.FXRate row -- every field optional."""

    source_funding_currency: str | None = None
    target_currency: str | None = None
    rate: float | None = None
    status: str | None = None


class FXRateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    fx_rate_id: int = Field(validation_alias="FXRateId")
    source_funding_currency: str | None = Field(default=None, validation_alias="SourceFundingCurrency")
    target_currency: str | None = Field(default=None, validation_alias="TargetCurrency")
    rate: float | None = Field(default=None, validation_alias="Rate")
    status: str | None = Field(default=None, validation_alias="Status")


# Fields the FXRate grid may sort by (server-side).
FXRateSortField = Literal[
    "fx_rate_id",
    "source_funding_currency",
    "target_currency",
    "rate",
    "status",
]
