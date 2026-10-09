from datetime import date

from sqlalchemy import BigInteger, Date, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class Project(GoldControlColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'Project_Master'). Types are inferred from column names -- confirm against a
    real export. Source-data table (gold schema); control columns come from GoldControlColumnsMixin."""

    __tablename__ = "Project"
    __table_args__ = {"schema": "gold"}

    ProjectId: Mapped[int] = mapped_column("Project_Id", BigInteger, primary_key=True)
    ProjectNumber: Mapped[str | None] = mapped_column(String(255))
    UPC: Mapped[str | None] = mapped_column(String(255))
    ProjectName: Mapped[str | None] = mapped_column(String(150))
    ContractNumber: Mapped[str | None] = mapped_column(String(255))
    LOBName: Mapped[str | None] = mapped_column("LOB_Name", String(150))
    CustomerNumber: Mapped[str | None] = mapped_column(String(255))
    CustomerName: Mapped[str | None] = mapped_column(String(150))
    LOBId: Mapped[int | None] = mapped_column("LOB_Id", BigInteger)
    ProductName: Mapped[str | None] = mapped_column(String(150))
    ProjectStartDate: Mapped[date | None] = mapped_column("Project_Start_Date", Date)
    ProjectEndDate: Mapped[date | None] = mapped_column("Project_End_Date", Date)
    ProjectStatus: Mapped[str | None] = mapped_column("Project_Status", String(255))
    ProjectCurrency: Mapped[str | None] = mapped_column("Project_Currency", String(255))
    ContractCurrency: Mapped[str | None] = mapped_column("Contract_Currency", String(255))
    LegalEntity: Mapped[str | None] = mapped_column("Legal_Entity", String(255))
    BusinessUnit: Mapped[str | None] = mapped_column("Business_Unit", String(255))
    Location: Mapped[str | None] = mapped_column(String(150))
    GLCompanyCode: Mapped[str | None] = mapped_column(String(255))
    QuotedFee: Mapped[float | None] = mapped_column(Numeric(18, 2))
    QuotedCost: Mapped[float | None] = mapped_column(Numeric(18, 2))
    Description: Mapped[str | None] = mapped_column(String(255))
    ProjectValue: Mapped[float | None] = mapped_column("Project_Value", Numeric(18, 2))
    Status: Mapped[str | None] = mapped_column(String(50))
    ChargeScale: Mapped[float | None] = mapped_column(Numeric(18, 2))
    PercentComplete: Mapped[float | None] = mapped_column("%Complete", Numeric(18, 2))
    ProjectManagerHRID: Mapped[str | None] = mapped_column("project_managerHRID", String(50))
    OversightDirectorHRID: Mapped[str | None] = mapped_column("oversight_directorHRID", String(50))
    OversightVpHRID: Mapped[str | None] = mapped_column("oversight_vpHRID", String(50))
    FinanceDirectorHRID: Mapped[str | None] = mapped_column("finance_directorHRID", String(50))
    FinancialAnalystHRID: Mapped[str | None] = mapped_column("financial_analystHRID", String(50))
    FinanceManagerHRID: Mapped[str | None] = mapped_column("finance_managerHRID", String(50))
    ProjectOrganization: Mapped[str | None] = mapped_column("Project_Organization", String(255))
    AgreedOverspend: Mapped[float | None] = mapped_column(Numeric(18, 2))
    PassthroughBudget: Mapped[float | None] = mapped_column(Numeric(18, 2))
    Budget: Mapped[float | None] = mapped_column(Numeric(18, 2))
