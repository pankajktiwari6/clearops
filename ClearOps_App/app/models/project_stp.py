from datetime import date, datetime

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, Numeric, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldAuditColumnsMixin


class ProjectSTP(GoldAuditColumnsMixin, Base):
    """Mirrors gold.ClearOps_ProjectSTP in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    ClearOps application-owned table. Audit/control columns come from GoldAuditColumnsMixin."""

    __tablename__ = "ClearOps_ProjectSTP"
    __table_args__ = {"schema": "gold"}

    ProjectSTPId: Mapped[int] = mapped_column("Project_STP_Id", BigInteger, primary_key=True)
    ResorceId: Mapped[int | None] = mapped_column("Resorce_id", BigInteger, ForeignKey("gold.Resources.Resource_ID"))
    RateCardId: Mapped[int | None] = mapped_column("Rate_Card_Id", BigInteger, ForeignKey("gold.ClearOps_RateCard.Rate_Card_Id"))
    TaskStartDate: Mapped[date | None] = mapped_column("task_start_date", Date)
    MonthlyValue: Mapped[float | None] = mapped_column("Monthly_Value", Numeric(18, 2))
    MonthlyHours: Mapped[float | None] = mapped_column("Monthly_Hours", Numeric(9, 2))
    TaskId: Mapped[int | None] = mapped_column("task_id", BigInteger, ForeignKey("gold.ProjectWBS.Project_WBS_Id"))
    YearMonths: Mapped[str | None] = mapped_column("Year_Months", String(20))
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime, server_default=func.sysutcdatetime())
