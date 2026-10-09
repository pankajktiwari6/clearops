from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import ClearOpsAuditColumnsMixin


class Login(ClearOpsAuditColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'ClearOps_login'). Types are inferred from column names -- confirm against a
    real export. ClearOps-owned table (clearops schema); audit columns come from ClearOpsAuditColumnsMixin."""

    __tablename__ = "Login"
    __table_args__ = {"schema": "clearops"}

    UserLoginId: Mapped[int] = mapped_column("user_login_Id", BigInteger, primary_key=True)
    SSO: Mapped[str | None] = mapped_column(String(255))
    Email: Mapped[str | None] = mapped_column(String(255))
    HRID: Mapped[str | None] = mapped_column(String(50))
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime)
