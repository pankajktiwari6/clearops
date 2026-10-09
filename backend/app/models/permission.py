from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import ClearOpsAuditColumnsMixin


class Permission(ClearOpsAuditColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'ClearOps_Permission'). Types are inferred from column names -- confirm against a
    real export. ClearOps-owned table (clearops schema); audit columns come from ClearOpsAuditColumnsMixin."""

    __tablename__ = "Permission"
    __table_args__ = {"schema": "clearops"}

    PermissionId: Mapped[int] = mapped_column("Permission_Id", BigInteger, primary_key=True)
    RoleId: Mapped[int | None] = mapped_column("Role_Id", BigInteger)
    PageId: Mapped[int | None] = mapped_column("Page_Id", BigInteger)
    HRIDempMstrtable: Mapped[str | None] = mapped_column(String(255))
    AccessId: Mapped[int | None] = mapped_column("Access_Id", BigInteger)
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime)
