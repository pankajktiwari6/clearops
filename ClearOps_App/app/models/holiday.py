from datetime import date
from uuid import UUID

from sqlalchemy import Date, Integer, LargeBinary, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldAuditColumnsMixin


class Holiday(GoldAuditColumnsMixin, Base):
    """Mirrors gold.ClearOps_Holiday in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    ClearOps application-owned table. Audit/control columns come from GoldAuditColumnsMixin."""

    __tablename__ = "ClearOps_Holiday"
    __table_args__ = {"schema": "gold"}

    HolidayId: Mapped[int] = mapped_column("Holiday_Id", Integer, primary_key=True)
    Country: Mapped[str] = mapped_column(String(100))
    HolidayDate: Mapped[date] = mapped_column(Date)
    Comment: Mapped[str | None] = mapped_column(String(500))
    HolidayName: Mapped[str | None] = mapped_column("Holiday_Name", String(200))
    SourceRowHash: Mapped[bytes | None] = mapped_column(LargeBinary)
    PipelineRunId: Mapped[UUID | None] = mapped_column(Uuid)
