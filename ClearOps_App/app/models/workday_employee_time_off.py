from datetime import date

from sqlalchemy import BigInteger, Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class WorkdayEmployeeTimeOff(GoldControlColumnsMixin, Base):
    """gold.ClearOps_Workday_Employee_TimeOff: Workday monthly time-off summary per resource. Added from Updated_ClearOps_Database_Final_fields.xlsx.
    Source-data table, loaded by the pipeline. Audit/control columns come from GoldControlColumnsMixin."""

    __tablename__ = "ClearOps_Workday_Employee_TimeOff"
    __table_args__ = {"schema": "gold"}

    WorkdayEmployeeTimeOffId: Mapped[int] = mapped_column("Workday_Employee_TimeOff_Id", BigInteger, primary_key=True, autoincrement=False)
    HRID: Mapped[str] = mapped_column(String(100), ForeignKey("gold.Employee_Master.HRID"))
    Month: Mapped[date] = mapped_column(Date)
    ScheduledWeeklyHours: Mapped[float | None] = mapped_column("Scheduled_Weekly_Hours", Numeric(6, 2))
    WorkingDays: Mapped[float | None] = mapped_column("Working_Days", Numeric(5, 2))
    ScheduledHours: Mapped[float | None] = mapped_column("Scheduled_Hours", Numeric(8, 2))
    PublicHolidayHours: Mapped[float | None] = mapped_column("Public_Holiday_Hours", Numeric(8, 2))
    PTOHours: Mapped[float | None] = mapped_column("PTO_Hours", Numeric(8, 2))
