from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldAuditColumnsMixin


class User(GoldAuditColumnsMixin, Base):
    """Mirrors gold.ClearOps_Users in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    ClearOps application-owned table. Audit/control columns come from GoldAuditColumnsMixin."""

    __tablename__ = "ClearOps_Users"
    __table_args__ = {"schema": "gold"}

    UserID: Mapped[int] = mapped_column("User_ID", BigInteger, primary_key=True)
    HRID: Mapped[str] = mapped_column(String(100), ForeignKey("gold.Employee_Master.HRID"))
    RoleId: Mapped[int | None] = mapped_column("Role_Id", Integer, ForeignKey("gold.ClearOps_Role.Role_Id"))
    RoleName: Mapped[str | None] = mapped_column("Role_Name", String(200))
    Name: Mapped[str | None] = mapped_column(String(400))
    Email: Mapped[str | None] = mapped_column(String(320))
    Module: Mapped[str | None] = mapped_column(String(100))
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime, server_default=func.sysutcdatetime())
