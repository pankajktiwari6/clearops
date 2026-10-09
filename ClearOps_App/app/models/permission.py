from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldAuditColumnsMixin


class Permission(GoldAuditColumnsMixin, Base):
    """Mirrors gold.ClearOps_Permission in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    ClearOps application-owned table. Audit/control columns come from GoldAuditColumnsMixin."""

    __tablename__ = "ClearOps_Permission"
    __table_args__ = {"schema": "gold"}

    PermissionId: Mapped[int] = mapped_column("Permission_Id", BigInteger, primary_key=True)
    RoleId: Mapped[int] = mapped_column("Role_Id", Integer, ForeignKey("gold.ClearOps_Role.Role_Id"))
    PageId: Mapped[int] = mapped_column("Page_Id", Integer, ForeignKey("gold.ClearOps_Page.Row_Id"))
    HRID: Mapped[str | None] = mapped_column(String(100), ForeignKey("gold.Employee_Master.HRID"))
    AccessId: Mapped[int] = mapped_column("Access_Id", Integer, ForeignKey("gold.ClearOps_Access_table.Access_ID"))
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime, server_default=func.sysutcdatetime())
