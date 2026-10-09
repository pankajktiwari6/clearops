from datetime import date

from sqlalchemy import BigInteger, Date, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import ClearOpsAuditColumnsMixin


class Resource(ClearOpsAuditColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'ClearOps_Resources'). Types are inferred from column names -- confirm against a
    real export. ClearOps-owned table (clearops schema); audit columns come from ClearOpsAuditColumnsMixin."""

    __tablename__ = "Resource"
    __table_args__ = {"schema": "clearops"}

    HRID: Mapped[str | None] = mapped_column(String(50))
    Name: Mapped[str | None] = mapped_column(String(150))
    StartDate: Mapped[date | None] = mapped_column(Date)
    EndDate: Mapped[date | None] = mapped_column(Date)
    GradeId: Mapped[int | None] = mapped_column("Grade_Id", BigInteger)
    Email: Mapped[str | None] = mapped_column(String(255))
    LOBId: Mapped[int | None] = mapped_column("LOB_Id", BigInteger)
    Budget: Mapped[float | None] = mapped_column(Numeric(18, 2))
    ResourceID: Mapped[int] = mapped_column("Resource_ID", BigInteger, primary_key=True)
    WeeklyHours: Mapped[float | None] = mapped_column(Numeric(18, 2))
    Status: Mapped[str | None] = mapped_column(String(50))
