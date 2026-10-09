from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldAuditColumnsMixin


class Login(GoldAuditColumnsMixin, Base):
    """Mirrors gold.ClearOps_login in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    ClearOps application-owned table. Audit/control columns come from GoldAuditColumnsMixin."""

    __tablename__ = "ClearOps_login"
    __table_args__ = {"schema": "gold"}

    UserLoginId: Mapped[int] = mapped_column("user_login_Id", BigInteger, primary_key=True)
    SSO: Mapped[str | None] = mapped_column(String(200))
    Email: Mapped[str | None] = mapped_column(String(320))
    HRID: Mapped[str] = mapped_column(String(100), ForeignKey("gold.Employee_Master.HRID"))
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime, server_default=func.sysutcdatetime())
