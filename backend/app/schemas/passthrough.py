from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PassthroughCreate(BaseModel):
    """Payload for creating a clearops.Passthrough row (primary key is generated)."""

    contract_number: str | None = None
    project_id: int | None = None
    transaction_id: int | None = None
    supplier_employee_name: str | None = None
    supplier_invoice_number: str | None = None
    expenditure_item_date: date | None = None
    transaction_row_cost: float | None = None
    transaction_currency: str | None = None


class PassthroughUpdate(BaseModel):
    """Partial update of a clearops.Passthrough row -- every field optional."""

    contract_number: str | None = None
    project_id: int | None = None
    transaction_id: int | None = None
    supplier_employee_name: str | None = None
    supplier_invoice_number: str | None = None
    expenditure_item_date: date | None = None
    transaction_row_cost: float | None = None
    transaction_currency: str | None = None


class PassthroughResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    contract_number: str | None = Field(default=None, validation_alias="ContractNumber")
    project_id: int | None = Field(default=None, validation_alias="ProjectID")
    transaction_id: int | None = Field(default=None, validation_alias="TransactionId")
    supplier_employee_name: str | None = Field(default=None, validation_alias="SupplierEmployeeName")
    supplier_invoice_number: str | None = Field(default=None, validation_alias="SupplierInvoiceNumber")
    expenditure_item_date: date | None = Field(default=None, validation_alias="ExpenditureItemDate")
    transaction_row_cost: float | None = Field(default=None, validation_alias="TransactionRowCost")
    transaction_currency: str | None = Field(default=None, validation_alias="TransactionCurrency")
    pass_through_id: int = Field(validation_alias="PassThroughId")


# Fields the Passthrough grid may sort by (server-side).
PassthroughSortField = Literal[
    "contract_number",
    "project_id",
    "transaction_id",
    "supplier_employee_name",
    "supplier_invoice_number",
    "expenditure_item_date",
    "transaction_row_cost",
    "transaction_currency",
    "pass_through_id",
]
