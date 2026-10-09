from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import ClearOpsAuditColumnsMixin


class Team(ClearOpsAuditColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'ClearOps_Teams'). Types are inferred from column names -- confirm against a
    real export. ClearOps-owned table (clearops schema); audit columns come from ClearOpsAuditColumnsMixin."""

    __tablename__ = "Team"
    __table_args__ = {"schema": "clearops"}

    TeamId: Mapped[int] = mapped_column("Team_Id", BigInteger, primary_key=True)
    TeamName: Mapped[str | None] = mapped_column(String(150))
    TeamMission: Mapped[str | None] = mapped_column(String(255))
    TeamLead: Mapped[str | None] = mapped_column(String(255))
    TeamMembers: Mapped[str | None] = mapped_column(String(255))
    ResourceId: Mapped[int | None] = mapped_column("Resource_Id", BigInteger)
    Teammanager: Mapped[str | None] = mapped_column("teammanager", String(255))
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime)
