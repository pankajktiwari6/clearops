from datetime import date, datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import SilverControlColumnsMixin


class SalesforceOpportunity(SilverControlColumnsMixin, Base):
    """Mirrors silver.SalesforceOpportunity in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    Source-data table, loaded by the pipeline. Audit/control columns come from SilverControlColumnsMixin."""

    __tablename__ = "SalesforceOpportunity"
    __table_args__ = {"schema": "silver"}

    SalesforceOpportunitySK: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    OpportunityID: Mapped[str] = mapped_column("Opportunity_ID", String(50))
    OpportunityCode: Mapped[str | None] = mapped_column("Opportunity_Code", String(100))
    Amount: Mapped[float | None] = mapped_column(Numeric(18, 2))
    TotalDirectFee: Mapped[float | None] = mapped_column("Total_Direct_Fee", Numeric(18, 2))
    ProjectCodeUPC: Mapped[str | None] = mapped_column("Project_Code/UPC", String(100))
    OwningBusinessUnitLOB: Mapped[str | None] = mapped_column("Owning_Business_Unit/LOB", String(150))
    ServiceArea: Mapped[str | None] = mapped_column("Service_Area", String(150))
    ServiceLine: Mapped[str | None] = mapped_column("Service_Line", String(150))
    KeyFieldsLastModifiedDate: Mapped[datetime | None] = mapped_column("Key_Fields_Last_Modified_Date", DateTime)
    StageName: Mapped[str | None] = mapped_column(String(100))
    SubStage: Mapped[str | None] = mapped_column("Sub_Stage", String(100))
    ShortDescription: Mapped[str | None] = mapped_column("Short_Description", Text)
    AssetName: Mapped[str | None] = mapped_column("Asset_Name", String(300))
    EstimatedProbabilityIn: Mapped[float | None] = mapped_column("Estimated_Probability_in", Numeric(9, 2))
    GeographicFocus: Mapped[str | None] = mapped_column("Geographic_Focus", String(100))
    PrimaryGeneralIndicationL2LIndication: Mapped[str | None] = mapped_column("Primary_General_Indication_L2L/Indication", String(255))
    RevenueRegion: Mapped[str | None] = mapped_column("Revenue_Region", String(150))
    PlannedProjectStartDate: Mapped[date | None] = mapped_column("Planned_Project_Start_Date", Date)
    PreviousProject: Mapped[str | None] = mapped_column("Previous_Project", String(100))
    ProductChannel: Mapped[str | None] = mapped_column("Product_Channel", String(150))
    ContractReceived: Mapped[date | None] = mapped_column("Contract_Received", Date)
    SalesStageAsOfDate: Mapped[date | None] = mapped_column("Sales_Stage_As_Of_Date", Date)
    ProductAttributes: Mapped[str | None] = mapped_column("Product_Attributes", Text)
    ProjectType: Mapped[str | None] = mapped_column("Project_Type", String(150))
    PlannedProjectDurationMonths: Mapped[float | None] = mapped_column("Planned_Project_Duration_Months", Numeric(9, 2))
    StartDate: Mapped[date | None] = mapped_column("Start_date", Date)
    PrimaryTherapeuticAreaL2L: Mapped[str | None] = mapped_column("Primary_Therapeutic_Area_L2L", String(255))
    WorkAhead: Mapped[bool | None] = mapped_column("Work_Ahead", Boolean)
    AddedToBT: Mapped[bool | None] = mapped_column("Added_to_BT", Boolean)
    BTCode: Mapped[str | None] = mapped_column("BT_Code", String(100))
    ClientSatScore: Mapped[float | None] = mapped_column("Client_Sat_Score", Numeric(9, 2))
    ClientName: Mapped[str | None] = mapped_column("Client_Name", String(300))
    OwnerEmail: Mapped[str | None] = mapped_column("Owner_Email", String(320))
    OwnerUsername: Mapped[str | None] = mapped_column("Owner_Username", String(320))
    OwnerFirstName: Mapped[str | None] = mapped_column("Owner.FirstName", String(100))
    OwnerLastName: Mapped[str | None] = mapped_column("Owner.LastName", String(100))
    CrosssolveICOpportunity: Mapped[bool | None] = mapped_column("Crosssolve_IC_Opportunity", Boolean)
    CrosssolvePrimaryOpportunity: Mapped[bool | None] = mapped_column("Crosssolve_Primary_Opportunity", Boolean)
    OriginatingOpportunityID: Mapped[str | None] = mapped_column("Originating_Opportunity_ID", String(50))
