from datetime import date, time

from sqlalchemy import BigInteger, Boolean, Date, ForeignKey, Numeric, String, Text, Time, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldAuditColumnsMixin


class ProjectTimePlanner(GoldAuditColumnsMixin, Base):
    """Mirrors gold.ClearOps_ProjectTimePlanner in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    ClearOps application-owned table. Audit/control columns come from GoldAuditColumnsMixin."""

    __tablename__ = "ClearOps_ProjectTimePlanner"
    __table_args__ = {"schema": "gold"}

    ProjectTimePannerId: Mapped[int] = mapped_column("Project_Time_Panner_id", BigInteger, primary_key=True)
    TaskID: Mapped[int | None] = mapped_column("Task_ID", BigInteger, ForeignKey("gold.ProjectWBS.Project_WBS_Id"))
    ResourceId: Mapped[int | None] = mapped_column("Resource_Id", BigInteger, ForeignKey("gold.Resources.Resource_ID"))
    StartDate: Mapped[date | None] = mapped_column(Date)
    EndDate: Mapped[date | None] = mapped_column(Date)
    StartTime: Mapped[time | None] = mapped_column(Time)
    EndTime: Mapped[time | None] = mapped_column(Time)
    PlanHours: Mapped[float | None] = mapped_column(Numeric(9, 2))
    Description: Mapped[str | None] = mapped_column(Text)
    CompletedStatus: Mapped[str | None] = mapped_column(String(30))
    IsActive: Mapped[bool] = mapped_column(Boolean, server_default=text("1"))
