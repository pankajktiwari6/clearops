from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldAuditColumnsMixin


class Role(GoldAuditColumnsMixin, Base):
    """Mirrors gold.ClearOps_Role in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    ClearOps application-owned table. Audit/control columns come from GoldAuditColumnsMixin."""

    __tablename__ = "ClearOps_Role"
    __table_args__ = {"schema": "gold"}

    RoleId: Mapped[int] = mapped_column("Role_Id", Integer, primary_key=True)
    RoleName: Mapped[str] = mapped_column("Role_Name", String(200))
    RoleType: Mapped[str | None] = mapped_column("Role_Type", String(50))
