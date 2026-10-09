from datetime import date, datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class ProjectWBS(GoldControlColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'ProjectWBS'). Types are inferred from column names -- confirm against a
    real export. Source-data table (gold schema); control columns come from GoldControlColumnsMixin."""

    __tablename__ = "ProjectWBS"
    __table_args__ = {"schema": "gold"}

    TaskId: Mapped[int | None] = mapped_column("Task_Id", BigInteger)
    ParentTaskID: Mapped[int | None] = mapped_column(BigInteger)
    WBSLevel: Mapped[str | None] = mapped_column("WBS_Level", String(255))
    TaskType: Mapped[str | None] = mapped_column("Task_Type", String(255))
    TaskName: Mapped[str | None] = mapped_column("Task_Name", String(150))
    TaskNumber: Mapped[str | None] = mapped_column("Task_Number", String(255))
    DeliveryType: Mapped[str | None] = mapped_column("Delivery_Type", String(255))
    TaskStartDate: Mapped[date | None] = mapped_column("Task_Start_Date", Date)
    TaskEndDate: Mapped[date | None] = mapped_column("Task_End_Date", Date)
    ChargeableFlag: Mapped[bool | None] = mapped_column("Chargeable_Flag", Boolean)
    BillableFlag: Mapped[bool | None] = mapped_column("Billable_Flag", Boolean)
    CurrentBudgetRevenue: Mapped[float | None] = mapped_column("CurrentBudget–Revenue", Numeric(18, 2))
    CurrentBudgetCost: Mapped[float | None] = mapped_column("CurrentBudget–Cost", Numeric(18, 2))
    ITDActuals: Mapped[float | None] = mapped_column("ITD_Actuals", Numeric(18, 2))
    ProjectId: Mapped[int | None] = mapped_column("Project_Id", BigInteger)
    TopTaskId: Mapped[int | None] = mapped_column("Top_Task_Id", BigInteger)
    ProjectWBSId: Mapped[int] = mapped_column("Project_WBS_Id", BigInteger, primary_key=True)
    CreatedBy: Mapped[str | None] = mapped_column(String(255))
    CreatedDate: Mapped[datetime | None] = mapped_column(DateTime)
    ModifiedBy: Mapped[str | None] = mapped_column(String(255))
    ModifiedDate: Mapped[datetime | None] = mapped_column(DateTime)
    PBU: Mapped[str | None] = mapped_column(String(255))
    ServiceTypeCode: Mapped[str | None] = mapped_column("Service_Type_Code", String(255))
    UPC: Mapped[str | None] = mapped_column(String(255))
    PeriodName: Mapped[str | None] = mapped_column("Period_Name", String(150))
