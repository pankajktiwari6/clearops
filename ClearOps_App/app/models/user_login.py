from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldAuditColumnsMixin


class UserLogin(GoldAuditColumnsMixin, Base):
    """Mirrors gold.ClearOps_UserLogin in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    ClearOps application-owned table. Audit/control columns come from GoldAuditColumnsMixin."""

    __tablename__ = "ClearOps_UserLogin"
    __table_args__ = {"schema": "gold"}

    Userid: Mapped[int] = mapped_column("userid", BigInteger, primary_key=True)
    Email: Mapped[str | None] = mapped_column("email", String(320))
    Logindatetimestampe: Mapped[datetime | None] = mapped_column("logindatetimestampe", DateTime)
    Status: Mapped[str | None] = mapped_column("status", String(30))
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime, server_default=func.sysutcdatetime())
