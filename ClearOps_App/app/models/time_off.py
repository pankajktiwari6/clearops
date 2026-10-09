from datetime import date

from sqlalchemy import BigInteger, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class TimeOff(GoldControlColumnsMixin, Base):
    """Mirrors gold.TimeOff_WD in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    Source-data table, loaded by the pipeline. Audit/control columns come from GoldControlColumnsMixin."""

    __tablename__ = "TimeOff_WD"
    __table_args__ = {"schema": "gold"}

    TimeOffId: Mapped[int] = mapped_column("Time_Off_Id", BigInteger, primary_key=True)
    HRID: Mapped[str] = mapped_column(String(100), ForeignKey("gold.Employee_Master.HRID"))
    TIMEOFFDATE: Mapped[date] = mapped_column("TIME_OFF_DATE", Date)
    TimeOFFTYPE: Mapped[str | None] = mapped_column("Time_OFF_TYPE", String(100))
    TYPEDAYSORHOURS: Mapped[str | None] = mapped_column("TYPE_DAYS_OR_HOURS", String(20))
    TimeDataApproved: Mapped[date | None] = mapped_column("Time_Data_Approved", Date)
