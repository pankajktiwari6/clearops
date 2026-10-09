from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldAuditColumnsMixin


class AdminIntegrationStatus(GoldAuditColumnsMixin, Base):
    """Mirrors gold.ClearOps_Admin_IntegrationStatus in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    ClearOps application-owned table. Audit/control columns come from GoldAuditColumnsMixin."""

    __tablename__ = "ClearOps_Admin_IntegrationStatus"
    __table_args__ = {"schema": "gold"}

    SysIntegrationId: Mapped[int] = mapped_column("sys_integration_id", Integer, primary_key=True)
    System: Mapped[str] = mapped_column(String(100))
    LastSync: Mapped[datetime | None] = mapped_column(DateTime)
    Status: Mapped[str | None] = mapped_column(String(30))
    RecordCaptured: Mapped[int | None] = mapped_column("record_captured", BigInteger)
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime, server_default=func.sysutcdatetime())
