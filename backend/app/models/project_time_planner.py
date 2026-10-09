from datetime import date, time

from sqlalchemy import BigInteger, Boolean, Date, Numeric, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class ProjectTimePlanner(GoldControlColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'ClearOps_ProjectTimePlanner'). Types are inferred from column names -- confirm against a
    real export. Gold control columns come from GoldControlColumnsMixin."""

    __tablename__ = "ProjectTimePlanner"
    __table_args__ = {"schema": "gold"}

    ProjectTimePannerId: Mapped[int] = mapped_column("Project_Time_Panner_id", BigInteger, primary_key=True)
    TaskID: Mapped[int | None] = mapped_column("Task_ID", BigInteger)
    ResourceId: Mapped[int | None] = mapped_column("Resource_Id", BigInteger)
    StartDate: Mapped[date | None] = mapped_column(Date)
    EndDate: Mapped[date | None] = mapped_column(Date)
    StartTime: Mapped[time | None] = mapped_column(Time)
    EndTime: Mapped[time | None] = mapped_column(Time)
    PlanHours: Mapped[float | None] = mapped_column(Numeric(18, 2))
    Description: Mapped[str | None] = mapped_column(String(255))
    CompletedStatus: Mapped[float | None] = mapped_column(Numeric(18, 2))
    IsActive: Mapped[bool | None] = mapped_column(Boolean)
