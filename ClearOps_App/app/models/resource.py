from datetime import date

from sqlalchemy import BigInteger, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class Resource(GoldControlColumnsMixin, Base):
    """Mirrors gold.Resources in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    Source-data table, loaded by the pipeline. Audit/control columns come from GoldControlColumnsMixin."""

    __tablename__ = "Resources"
    __table_args__ = {"schema": "gold"}

    ResourceID: Mapped[int] = mapped_column("Resource_ID", BigInteger, primary_key=True)
    HRID: Mapped[str] = mapped_column(String(100), ForeignKey("gold.Employee_Master.HRID"))
    Name: Mapped[str | None] = mapped_column(String(400))
    StartDate: Mapped[date | None] = mapped_column(Date)
    EndDate: Mapped[date | None] = mapped_column(Date)
    GradeId: Mapped[int | None] = mapped_column("Grade_Id", Integer, ForeignKey("gold.Grades.Grade_Id"))
    Email: Mapped[str | None] = mapped_column(String(320))
    LOBId: Mapped[int | None] = mapped_column("LOB_Id", Integer, ForeignKey("gold.LOB.LOB_Id"))
    Budget: Mapped[float | None] = mapped_column(Numeric(18, 2))
    WeeklyHours: Mapped[float | None] = mapped_column(Numeric(6, 2))
    Status: Mapped[str | None] = mapped_column(String(30))
