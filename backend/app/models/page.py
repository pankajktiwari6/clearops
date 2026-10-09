from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class Page(GoldControlColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'ClearOps_Page'). Types are inferred from column names -- confirm against a
    real export. Gold control columns come from GoldControlColumnsMixin."""

    __tablename__ = "Page"
    __table_args__ = {"schema": "gold"}

    RowId: Mapped[int] = mapped_column("Row_Id", BigInteger, primary_key=True)
    PageNumber: Mapped[str | None] = mapped_column("Page_Number", String(255))
    PageName: Mapped[str | None] = mapped_column("Page_Name", String(150))
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime)
