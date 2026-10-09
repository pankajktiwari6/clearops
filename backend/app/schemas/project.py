from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    """Payload for creating a gold.Project_Master row (identity key and audit columns are generated)."""

    project_number: str
    upc: str | None = None
    project_name: str | None = None
    contract_number: str | None = None
    lob_name: str | None = None
    customer_number: str | None = None
    customer_name: str | None = None
    lob_id: int | None = None
    product_name: str | None = None
    project_start_date: date | None = None
    project_end_date: date | None = None
    project_status: str | None = None
    project_currency: str | None = None
    contract_currency: str | None = None
    legal_entity: str | None = None
    business_unit: str | None = None
    location: str | None = None
    gl_company_code: str | None = None
    quoted_fee: float | None = None
    quoted_cost: float | None = None
    description: str | None = None
    project_value: float | None = None
    status: str | None = None
    charge_scale: str | None = None
    percent_complete: float | None = None
    project_manager_hrid: str | None = None
    oversight_director_hrid: str | None = None
    oversight_vp_hrid: str | None = None
    finance_director_hrid: str | None = None
    financial_analyst_hrid: str | None = None
    finance_manager_hrid: str | None = None
    project_organization: str | None = None
    agreed_overspend: float | None = None
    passthrough_budget: float | None = None
    budget: float | None = None


class ProjectUpdate(BaseModel):
    """Partial update of a gold.Project_Master row -- every field optional."""

    project_number: str | None = None
    upc: str | None = None
    project_name: str | None = None
    contract_number: str | None = None
    lob_name: str | None = None
    customer_number: str | None = None
    customer_name: str | None = None
    lob_id: int | None = None
    product_name: str | None = None
    project_start_date: date | None = None
    project_end_date: date | None = None
    project_status: str | None = None
    project_currency: str | None = None
    contract_currency: str | None = None
    legal_entity: str | None = None
    business_unit: str | None = None
    location: str | None = None
    gl_company_code: str | None = None
    quoted_fee: float | None = None
    quoted_cost: float | None = None
    description: str | None = None
    project_value: float | None = None
    status: str | None = None
    charge_scale: str | None = None
    percent_complete: float | None = None
    project_manager_hrid: str | None = None
    oversight_director_hrid: str | None = None
    oversight_vp_hrid: str | None = None
    finance_director_hrid: str | None = None
    financial_analyst_hrid: str | None = None
    finance_manager_hrid: str | None = None
    project_organization: str | None = None
    agreed_overspend: float | None = None
    passthrough_budget: float | None = None
    budget: float | None = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    project_id: int = Field(validation_alias="ProjectId")
    project_number: str = Field(validation_alias="ProjectNumber")
    upc: str | None = Field(default=None, validation_alias="UPC")
    project_name: str | None = Field(default=None, validation_alias="ProjectName")
    contract_number: str | None = Field(default=None, validation_alias="ContractNumber")
    lob_name: str | None = Field(default=None, validation_alias="LOBName")
    customer_number: str | None = Field(default=None, validation_alias="CustomerNumber")
    customer_name: str | None = Field(default=None, validation_alias="CustomerName")
    lob_id: int | None = Field(default=None, validation_alias="LOBId")
    product_name: str | None = Field(default=None, validation_alias="ProductName")
    project_start_date: date | None = Field(default=None, validation_alias="ProjectStartDate")
    project_end_date: date | None = Field(default=None, validation_alias="ProjectEndDate")
    project_status: str | None = Field(default=None, validation_alias="ProjectStatus")
    project_currency: str | None = Field(default=None, validation_alias="ProjectCurrency")
    contract_currency: str | None = Field(default=None, validation_alias="ContractCurrency")
    legal_entity: str | None = Field(default=None, validation_alias="LegalEntity")
    business_unit: str | None = Field(default=None, validation_alias="BusinessUnit")
    location: str | None = Field(default=None, validation_alias="Location")
    gl_company_code: str | None = Field(default=None, validation_alias="GLCompanyCode")
    quoted_fee: float | None = Field(default=None, validation_alias="QuotedFee")
    quoted_cost: float | None = Field(default=None, validation_alias="QuotedCost")
    description: str | None = Field(default=None, validation_alias="Description")
    project_value: float | None = Field(default=None, validation_alias="ProjectValue")
    status: str | None = Field(default=None, validation_alias="Status")
    charge_scale: str | None = Field(default=None, validation_alias="ChargeScale")
    percent_complete: float | None = Field(default=None, validation_alias="PercentComplete")
    project_manager_hrid: str | None = Field(default=None, validation_alias="ProjectManagerHRID")
    oversight_director_hrid: str | None = Field(default=None, validation_alias="OversightDirectorHRID")
    oversight_vp_hrid: str | None = Field(default=None, validation_alias="OversightVpHRID")
    finance_director_hrid: str | None = Field(default=None, validation_alias="FinanceDirectorHRID")
    financial_analyst_hrid: str | None = Field(default=None, validation_alias="FinancialAnalystHRID")
    finance_manager_hrid: str | None = Field(default=None, validation_alias="FinanceManagerHRID")
    project_organization: str | None = Field(default=None, validation_alias="ProjectOrganization")
    agreed_overspend: float | None = Field(default=None, validation_alias="AgreedOverspend")
    passthrough_budget: float | None = Field(default=None, validation_alias="PassthroughBudget")
    budget: float | None = Field(default=None, validation_alias="Budget")


# Fields the Project grid may sort by (server-side).
ProjectSortField = Literal[
    "project_id",
    "project_number",
    "upc",
    "project_name",
    "contract_number",
    "lob_name",
    "customer_number",
    "customer_name",
    "lob_id",
    "product_name",
    "project_start_date",
    "project_end_date",
    "project_status",
    "project_currency",
    "contract_currency",
    "legal_entity",
    "business_unit",
    "location",
    "gl_company_code",
    "quoted_fee",
    "quoted_cost",
    "description",
    "project_value",
    "status",
    "charge_scale",
    "percent_complete",
    "project_manager_hrid",
    "oversight_director_hrid",
    "oversight_vp_hrid",
    "finance_director_hrid",
    "financial_analyst_hrid",
    "finance_manager_hrid",
    "project_organization",
    "agreed_overspend",
    "passthrough_budget",
    "budget",
]
