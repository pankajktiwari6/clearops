from datetime import date

from sqlalchemy import BigInteger, Boolean, Date, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class TimeOff(GoldControlColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'TimeOff(WD)'). Types are inferred from column names -- confirm against a
    real export. Source-data table (gold schema); control columns come from GoldControlColumnsMixin."""

    __tablename__ = "TimeOff"
    __table_args__ = {"schema": "gold"}

    TimeOffId: Mapped[int] = mapped_column("Time_Off_Id", BigInteger, primary_key=True)
    HRID: Mapped[str | None] = mapped_column(String(50))
    TIMEOFFDATE: Mapped[date | None] = mapped_column("TIME_OFF_DATE", Date)
    TimeOFFTYPE: Mapped[str | None] = mapped_column("Time_OFF_TYPE", String(255))
    TYPEDAYSORHOURS: Mapped[str | None] = mapped_column("TYPE_DAYS_OR_HOURS", String(50))
    TimeDataApproved: Mapped[bool | None] = mapped_column("Time_Data_Approved", Boolean)
