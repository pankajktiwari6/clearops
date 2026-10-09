from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldAuditColumnsMixin


class Team(GoldAuditColumnsMixin, Base):
    """Mirrors gold.ClearOps_Teams in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    ClearOps application-owned table. Audit/control columns come from GoldAuditColumnsMixin."""

    __tablename__ = "ClearOps_Teams"
    __table_args__ = {"schema": "gold"}

    TeamId: Mapped[int] = mapped_column("Team_Id", Integer, primary_key=True)
    TeamName: Mapped[str] = mapped_column(String(200))
    TeamMission: Mapped[str | None] = mapped_column(String(1000))
    TeamLead: Mapped[str | None] = mapped_column(String(200))
    TeamMembers: Mapped[str | None] = mapped_column(Text)
    ResourceId: Mapped[int | None] = mapped_column("Resource_Id", BigInteger, ForeignKey("gold.Resources.Resource_ID"))
    Teammanager: Mapped[str | None] = mapped_column("teammanager", String(200))
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime, server_default=func.sysutcdatetime())
