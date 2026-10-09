from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SalesforceOpportunityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, validate_by_alias=True)

    salesforce_opportunity_sk: int = Field(validation_alias="SalesforceOpportunitySK")
    opportunity_id: str = Field(validation_alias="OpportunityID")
    opportunity_code: str | None = Field(default=None, validation_alias="OpportunityCode")
    amount: float | None = Field(default=None, validation_alias="Amount")
    total_direct_fee: float | None = Field(default=None, validation_alias="TotalDirectFee")
    project_code_upc: str | None = Field(default=None, validation_alias="ProjectCodeUPC")
    owning_business_unit_lob: str | None = Field(default=None, validation_alias="OwningBusinessUnitLOB")
    service_area: str | None = Field(default=None, validation_alias="ServiceArea")
    service_line: str | None = Field(default=None, validation_alias="ServiceLine")
    key_fields_last_modified_date: datetime | None = Field(default=None, validation_alias="KeyFieldsLastModifiedDate")
    stage_name: str | None = Field(default=None, validation_alias="StageName")
    sub_stage: str | None = Field(default=None, validation_alias="SubStage")
    short_description: str | None = Field(default=None, validation_alias="ShortDescription")
    asset_name: str | None = Field(default=None, validation_alias="AssetName")
    estimated_probability_in: float | None = Field(default=None, validation_alias="EstimatedProbabilityIn")
    geographic_focus: str | None = Field(default=None, validation_alias="GeographicFocus")
    primary_general_indication_l2_l_indication: str | None = Field(default=None, validation_alias="PrimaryGeneralIndicationL2LIndication")
    revenue_region: str | None = Field(default=None, validation_alias="RevenueRegion")
    planned_project_start_date: date | None = Field(default=None, validation_alias="PlannedProjectStartDate")
    previous_project: str | None = Field(default=None, validation_alias="PreviousProject")
    product_channel: str | None = Field(default=None, validation_alias="ProductChannel")
    contract_received: date | None = Field(default=None, validation_alias="ContractReceived")
    sales_stage_as_of_date: date | None = Field(default=None, validation_alias="SalesStageAsOfDate")
    product_attributes: str | None = Field(default=None, validation_alias="ProductAttributes")
    project_type: str | None = Field(default=None, validation_alias="ProjectType")
    planned_project_duration_months: float | None = Field(default=None, validation_alias="PlannedProjectDurationMonths")
    start_date: date | None = Field(default=None, validation_alias="StartDate")
    primary_therapeutic_area_l2_l: str | None = Field(default=None, validation_alias="PrimaryTherapeuticAreaL2L")
    work_ahead: bool | None = Field(default=None, validation_alias="WorkAhead")
    added_to_bt: bool | None = Field(default=None, validation_alias="AddedToBT")
    bt_code: str | None = Field(default=None, validation_alias="BTCode")
    client_sat_score: float | None = Field(default=None, validation_alias="ClientSatScore")
    client_name: str | None = Field(default=None, validation_alias="ClientName")
    owner_email: str | None = Field(default=None, validation_alias="OwnerEmail")
    owner_username: str | None = Field(default=None, validation_alias="OwnerUsername")
    owner_first_name: str | None = Field(default=None, validation_alias="OwnerFirstName")
    owner_last_name: str | None = Field(default=None, validation_alias="OwnerLastName")
    crosssolve_ic_opportunity: bool | None = Field(default=None, validation_alias="CrosssolveICOpportunity")
    crosssolve_primary_opportunity: bool | None = Field(default=None, validation_alias="CrosssolvePrimaryOpportunity")
    originating_opportunity_id: str | None = Field(default=None, validation_alias="OriginatingOpportunityID")


# Fields the SalesforceOpportunity grid may sort by (server-side).
SalesforceOpportunitySortField = Literal[
    "salesforce_opportunity_sk",
    "opportunity_id",
    "opportunity_code",
    "amount",
    "total_direct_fee",
    "project_code_upc",
    "owning_business_unit_lob",
    "service_area",
    "service_line",
    "key_fields_last_modified_date",
    "stage_name",
    "sub_stage",
    "short_description",
    "asset_name",
    "estimated_probability_in",
    "geographic_focus",
    "primary_general_indication_l2_l_indication",
    "revenue_region",
    "planned_project_start_date",
    "previous_project",
    "product_channel",
    "contract_received",
    "sales_stage_as_of_date",
    "product_attributes",
    "project_type",
    "planned_project_duration_months",
    "start_date",
    "primary_therapeutic_area_l2_l",
    "work_ahead",
    "added_to_bt",
    "bt_code",
    "client_sat_score",
    "client_name",
    "owner_email",
    "owner_username",
    "owner_first_name",
    "owner_last_name",
    "crosssolve_ic_opportunity",
    "crosssolve_primary_opportunity",
    "originating_opportunity_id",
]
