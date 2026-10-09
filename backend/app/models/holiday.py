from datetime import date

from sqlalchemy import BigInteger, Date, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class Holiday(GoldControlColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'ClearOps_Holiday'). Types are inferred from column names -- confirm against a
    real export. Gold control columns come from GoldControlColumnsMixin."""

    __tablename__ = "Holiday"
    __table_args__ = {"schema": "gold"}

    Country: Mapped[str | None] = mapped_column(String(150))
    HolidayDate: Mapped[date | None] = mapped_column(Date)
    Comment: Mapped[str | None] = mapped_column(String(255))
    HolidayId: Mapped[int] = mapped_column("Holiday_Id", BigInteger, primary_key=True)
    HolidayName: Mapped[str | None] = mapped_column("Holiday_Name", String(150))
