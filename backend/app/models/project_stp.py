from datetime import date, datetime

from sqlalchemy import BigInteger, Date, DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import ClearOpsAuditColumnsMixin


class ProjectSTP(ClearOpsAuditColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'ClearOps_ProjectSTP'). Types are inferred from column names -- confirm against a
    real export. ClearOps-owned table (clearops schema); audit columns come from ClearOpsAuditColumnsMixin."""

    __tablename__ = "ProjectSTP"
    __table_args__ = {"schema": "clearops"}

    ResorceId: Mapped[int | None] = mapped_column("Resorce_id", BigInteger)
    RateCardId: Mapped[int | None] = mapped_column("Rate_Card_Id", BigInteger)
    TaskStartDate: Mapped[date | None] = mapped_column("task_start_date", Date)
    MonthlyValue: Mapped[float | None] = mapped_column("Monthly_Value", Numeric(18, 2))
    MonthlyHours: Mapped[float | None] = mapped_column("Monthly_Hours", Numeric(18, 2))
    TaskId: Mapped[int | None] = mapped_column("task_id", BigInteger)
    YearMonths: Mapped[str | None] = mapped_column("Year_Months", String(255))
    ProjectSTPId: Mapped[int] = mapped_column("Project_STP_Id", BigInteger, primary_key=True)
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime)
