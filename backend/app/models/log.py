from datetime import datetime

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import ClearOpsAuditColumnsMixin


class Log(ClearOpsAuditColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'ClearOps_Logs_table'). Types are inferred from column names -- confirm against a
    real export. ClearOps-owned table (clearops schema); audit columns come from ClearOpsAuditColumnsMixin."""

    __tablename__ = "Log"
    __table_args__ = {"schema": "clearops"}

    LogId: Mapped[int] = mapped_column("log_id", BigInteger, primary_key=True)
    SysIntegrationId: Mapped[int | None] = mapped_column("sys_integration_id", BigInteger)
    CornjobrunId: Mapped[int | None] = mapped_column("cornjobrun_id", BigInteger)
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime)
