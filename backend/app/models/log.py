from datetime import datetime

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class Log(GoldControlColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'ClearOps_Logs_table'). Types are inferred from column names -- confirm against a
    real export. Gold control columns come from GoldControlColumnsMixin."""

    __tablename__ = "Log"
    __table_args__ = {"schema": "gold"}

    LogId: Mapped[int] = mapped_column("log_id", BigInteger, primary_key=True)
    SysIntegrationId: Mapped[int | None] = mapped_column("sys_integration_id", BigInteger)
    CornjobrunId: Mapped[int | None] = mapped_column("cornjobrun_id", BigInteger)
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime)
