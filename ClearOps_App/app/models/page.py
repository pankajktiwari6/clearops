from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldAuditColumnsMixin


class Page(GoldAuditColumnsMixin, Base):
    """Mirrors gold.ClearOps_Page in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    ClearOps application-owned table. Audit/control columns come from GoldAuditColumnsMixin."""

    __tablename__ = "ClearOps_Page"
    __table_args__ = {"schema": "gold"}

    RowId: Mapped[int] = mapped_column("Row_Id", Integer, primary_key=True)
    PageNumber: Mapped[int | None] = mapped_column("Page_Number", Integer)
    PageName: Mapped[str] = mapped_column("Page_Name", String(200))
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime, server_default=func.sysutcdatetime())
