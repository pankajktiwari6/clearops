from datetime import datetime

from sqlalchemy import JSON, BigInteger, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldAuditColumnsMixin


class ProjectSTPSetting(GoldAuditColumnsMixin, Base):
    """gold.ClearOps_STPSettings -- a user's saved Strategic Time Planner project filter ("saved query").
    ClearOps application-owned table. Audit columns come from GoldAuditColumnsMixin."""

    __tablename__ = "ClearOps_STPSettings"
    __table_args__ = (
        UniqueConstraint("User_Id", "Filter_Name", name="UQ_STPSettings_User_Filter"),
        {"schema": "gold"},
    )

    STPSettingId: Mapped[int] = mapped_column("STP_Setting_Id", BigInteger, primary_key=True)
    UserId: Mapped[int] = mapped_column("User_Id", BigInteger, ForeignKey("gold.ClearOps_Users.User_ID"))
    FilterName: Mapped[str] = mapped_column("Filter_Name", String(200))
    ProjectIds: Mapped[list] = mapped_column("Project_Ids", JSON)  # list of Project_Master.Project_Id
    SelectedProjects: Mapped[dict | None] = mapped_column("Selected_Projects", JSON)  # {id: {name, number, ...}}
    DateTime: Mapped[datetime | None] = mapped_column("Date_Time", DateTime, server_default=func.sysutcdatetime())
