from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import ClearOpsAuditColumnsMixin


class User(ClearOpsAuditColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'ClearOps_Users'). Types are inferred from column names -- confirm against a
    real export. ClearOps-owned table (clearops schema); audit columns come from ClearOpsAuditColumnsMixin."""

    __tablename__ = "User"
    __table_args__ = {"schema": "clearops"}

    HRID: Mapped[str | None] = mapped_column(String(50))
    RoleId: Mapped[int | None] = mapped_column("Role_Id", BigInteger)
    RoleName: Mapped[str | None] = mapped_column("Role_Name", String(150))
    Name: Mapped[str | None] = mapped_column(String(150))
    Email: Mapped[str | None] = mapped_column(String(255))
    UserID: Mapped[int] = mapped_column("User_ID", BigInteger, primary_key=True)
    Module: Mapped[str | None] = mapped_column(String(255))
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime)
