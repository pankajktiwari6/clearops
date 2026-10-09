from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldAuditColumnsMixin


class Access(GoldAuditColumnsMixin, Base):
    """Mirrors gold.ClearOps_Access_table in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    ClearOps application-owned table. Audit/control columns come from GoldAuditColumnsMixin."""

    __tablename__ = "ClearOps_Access_table"
    __table_args__ = {"schema": "gold"}

    AccessID: Mapped[int] = mapped_column("Access_ID", Integer, primary_key=True)
    AccrssType: Mapped[str] = mapped_column("Accrss_type", String(50))
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime, server_default=func.sysutcdatetime())
