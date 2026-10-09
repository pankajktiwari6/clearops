from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class ProjectWBS(GoldControlColumnsMixin, Base):
    """Mirrors gold.ProjectWBS in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    Source-data table, loaded by the pipeline. Audit/control columns come from GoldControlColumnsMixin."""

    __tablename__ = "ProjectWBS"
    __table_args__ = {"schema": "gold"}

    ProjectWBSId: Mapped[int] = mapped_column("Project_WBS_Id", BigInteger, primary_key=True)
    TaskId: Mapped[str | None] = mapped_column("Task_Id", String(50))
    ParentTaskID: Mapped[str | None] = mapped_column(String(124))
    WBSLevel: Mapped[str | None] = mapped_column("WBS_Level", String(20))
    TaskType: Mapped[str | None] = mapped_column("Task_Type", String(30))
    TaskName: Mapped[str | None] = mapped_column("Task_Name", String(500))
    TaskNumber: Mapped[str] = mapped_column("Task_Number", String(124))
    DeliveryType: Mapped[str | None] = mapped_column("Delivery_Type", String(100))
    TaskStartDate: Mapped[datetime | None] = mapped_column("Task_Start_Date", DateTime)
    TaskEndDate: Mapped[datetime | None] = mapped_column("Task_End_Date", DateTime)
    ChargeableFlag: Mapped[bool | None] = mapped_column("Chargeable_Flag", Boolean)
    BillableFlag: Mapped[bool | None] = mapped_column("Billable_Flag", Boolean)
    CurrentBudgetRevenueByTask: Mapped[float | None] = mapped_column("CurrentBudget_Revenue_ByTask", Numeric(18, 2))
    CurrentBudgetCostByTask: Mapped[float | None] = mapped_column("CurrentBudget_Cost_ByTask", Numeric(18, 2))
    ITDActualsHours: Mapped[float | None] = mapped_column("ITD_Actuals_Hours", Numeric(18, 2))
    ProjectId: Mapped[int] = mapped_column("Project_Id", BigInteger, ForeignKey("gold.Project_Master.Project_Id"))
    TopTaskId: Mapped[str | None] = mapped_column("Top_Task_Id", String(50))
    CreatedBy: Mapped[str | None] = mapped_column(String(100))
    CreatedDate: Mapped[datetime | None] = mapped_column(DateTime)
    ModifiedBy: Mapped[str | None] = mapped_column(String(100))
    ModifiedDate: Mapped[datetime | None] = mapped_column(DateTime)
    PBU: Mapped[str | None] = mapped_column(String(200))
    ServiceTypeCode: Mapped[str | None] = mapped_column("Service_Type_Code", String(100))
    UPC: Mapped[str | None] = mapped_column(String(40))
    PeriodName: Mapped[str | None] = mapped_column("Period_Name", String(64))
