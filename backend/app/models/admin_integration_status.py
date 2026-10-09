from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class AdminIntegrationStatus(GoldControlColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'ClearOps_Admin_IntegrationStatus'). Types are inferred from column names -- confirm against a
    real export. Gold control columns come from GoldControlColumnsMixin."""

    __tablename__ = "AdminIntegrationStatus"
    __table_args__ = {"schema": "gold"}

    System: Mapped[str | None] = mapped_column(String(255))
    LastSync: Mapped[datetime | None] = mapped_column(DateTime)
    Status: Mapped[str | None] = mapped_column(String(50))
    RecordCaptured: Mapped[str | None] = mapped_column("record_captured", String(255))
    SysIntegrationId: Mapped[int] = mapped_column("sys_integration_id", BigInteger, primary_key=True)
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime)
