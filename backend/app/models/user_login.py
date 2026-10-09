from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import ClearOpsAuditColumnsMixin


class UserLogin(ClearOpsAuditColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'ClearOps_UserLogin'). Types are inferred from column names -- confirm against a
    real export. ClearOps-owned table (clearops schema); audit columns come from ClearOpsAuditColumnsMixin."""

    __tablename__ = "UserLogin"
    __table_args__ = {"schema": "clearops"}

    Userid: Mapped[int] = mapped_column("userid", BigInteger, primary_key=True)
    Email: Mapped[str | None] = mapped_column("email", String(255))
    Logindatetimestampe: Mapped[datetime | None] = mapped_column("logindatetimestampe", DateTime)
    Status: Mapped[str | None] = mapped_column("status", String(50))
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime)
