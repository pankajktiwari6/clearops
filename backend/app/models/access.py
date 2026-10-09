from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class Access(GoldControlColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'ClearOpps_Access_table'). Types are inferred from column names -- confirm against a
    real export. Gold control columns come from GoldControlColumnsMixin."""

    __tablename__ = "Access"
    __table_args__ = {"schema": "gold"}

    AccessID: Mapped[int] = mapped_column("Access_ID", BigInteger, primary_key=True)
    AccrssType: Mapped[str | None] = mapped_column("Accrss_type", String(50))
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime)
