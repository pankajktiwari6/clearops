from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldAuditColumnsMixin


class Log(GoldAuditColumnsMixin, Base):
    """Mirrors gold.ClearOps_Logs_table in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    ClearOps application-owned table. Audit/control columns come from GoldAuditColumnsMixin."""

    __tablename__ = "ClearOps_Logs_table"
    __table_args__ = {"schema": "gold"}

    LogId: Mapped[int] = mapped_column("log_id", BigInteger, primary_key=True)
    SysIntegrationId: Mapped[int | None] = mapped_column("sys_integration_id", Integer, ForeignKey("gold.ClearOps_Admin_IntegrationStatus.sys_integration_id"))
    CornjobRunId: Mapped[str | None] = mapped_column("Cornjob_Run_Id", String(100))
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime, server_default=func.sysutcdatetime())
