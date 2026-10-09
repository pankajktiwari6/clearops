from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class RateCardCreate(BaseModel):
    """Payload for creating a gold.RateCard row (primary key is generated)."""

    client_code: str | None = None
    grade_id: int | None = None
    desciption: str | None = None
    rate: float | None = None
    rate_type: str | None = None
    rate_card_start_date: date | None = None
    rate_card_end_date: date | None = None
    transacton_currency: str | None = None
    country: str | None = None


class RateCardUpdate(BaseModel):
    """Partial update of a gold.RateCard row -- every field optional."""

    client_code: str | None = None
    grade_id: int | None = None
    desciption: str | None = None
    rate: float | None = None
    rate_type: str | None = None
    rate_card_start_date: date | None = None
    rate_card_end_date: date | None = None
    transacton_currency: str | None = None
    country: str | None = None


class RateCardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    client_code: str | None = Field(default=None, validation_alias="ClientCode")
    grade_id: int | None = Field(default=None, validation_alias="GradeId")
    desciption: str | None = Field(default=None, validation_alias="Desciption")
    rate: float | None = Field(default=None, validation_alias="Rate")
    rate_type: str | None = Field(default=None, validation_alias="RateType")
    rate_card_start_date: date | None = Field(default=None, validation_alias="RateCardStartDate")
    rate_card_end_date: date | None = Field(default=None, validation_alias="RateCardEndDate")
    transacton_currency: str | None = Field(default=None, validation_alias="TransactonCurrency")
    rate_card_id: int = Field(validation_alias="RateCardId")
    country: str | None = Field(default=None, validation_alias="Country")


# Fields the RateCard grid may sort by (server-side).
RateCardSortField = Literal[
    "client_code",
    "grade_id",
    "desciption",
    "rate",
    "rate_type",
    "rate_card_start_date",
    "rate_card_end_date",
    "transacton_currency",
    "rate_card_id",
    "country",
]
