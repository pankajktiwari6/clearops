from datetime import date

from sqlalchemy import BigInteger, Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class Project(GoldControlColumnsMixin, Base):
    """Mirrors gold.Project_Master in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    Source-data table, loaded by the pipeline. Audit/control columns come from GoldControlColumnsMixin."""

    __tablename__ = "Project_Master"
    __table_args__ = {"schema": "gold"}

    ProjectId: Mapped[int] = mapped_column("Project_Id", BigInteger, primary_key=True)
    ProjectNumber: Mapped[str] = mapped_column(String(450))
    UPC: Mapped[str | None] = mapped_column(String(450))
    ProjectName: Mapped[str | None] = mapped_column(String(450))
    ContractNumber: Mapped[str | None] = mapped_column(String(450))
    LOBName: Mapped[str | None] = mapped_column("LOB_Name", String(450))
    CustomerNumber: Mapped[str | None] = mapped_column(String(100))
    CustomerName: Mapped[str | None] = mapped_column(String(450))
    LOBId: Mapped[int | None] = mapped_column("LOB_Id", Integer, ForeignKey("gold.LOB.LOB_Id"))
    ProductName: Mapped[str | None] = mapped_column(String(450))
    ProjectStartDate: Mapped[date | None] = mapped_column("Project_Start_Date", Date)
    ProjectEndDate: Mapped[date | None] = mapped_column("Project_End_Date", Date)
    ProjectStatus: Mapped[str | None] = mapped_column("Project_Status", String(200))
    ProjectCurrency: Mapped[str | None] = mapped_column("Project_Currency", String(100))
    ContractCurrency: Mapped[str | None] = mapped_column("Contract_Currency", String(100))
    LegalEntity: Mapped[str | None] = mapped_column("Legal_Entity", String(450))
    BusinessUnit: Mapped[str | None] = mapped_column("Business_Unit", String(450))
    Location: Mapped[str | None] = mapped_column(String(450))
    GLCompanyCode: Mapped[str | None] = mapped_column(String(450))
    QuotedFee: Mapped[float | None] = mapped_column(Numeric(18, 2))
    QuotedCost: Mapped[float | None] = mapped_column(Numeric(18, 2))
    Description: Mapped[str | None] = mapped_column(Text)
    ProjectValue: Mapped[float | None] = mapped_column("Project_Value", Numeric(18, 2))
    Status: Mapped[str | None] = mapped_column(String(200))
    ChargeScale: Mapped[str | None] = mapped_column(String(100))
    PercentComplete: Mapped[float | None] = mapped_column("Percent_Complete", Numeric(9, 2))
    ProjectManagerHRID: Mapped[str | None] = mapped_column("project_managerHRID", String(100))
    OversightDirectorHRID: Mapped[str | None] = mapped_column("oversight_directorHRID", String(100))
    OversightVpHRID: Mapped[str | None] = mapped_column("oversight_vpHRID", String(100))
    FinanceDirectorHRID: Mapped[str | None] = mapped_column("finance_directorHRID", String(100))
    FinancialAnalystHRID: Mapped[str | None] = mapped_column("financial_analystHRID", String(100))
    FinanceManagerHRID: Mapped[str | None] = mapped_column("finance_managerHRID", String(100))
    ProjectOrganization: Mapped[str | None] = mapped_column("Project_Organization", String(450))
    AgreedOverspend: Mapped[float | None] = mapped_column(Numeric(18, 2))
    PassthroughBudget: Mapped[float | None] = mapped_column(Numeric(18, 2))
    Budget: Mapped[float | None] = mapped_column(Numeric(18, 2))
