from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class Role(GoldControlColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'ClearOps_Role'). Types are inferred from column names -- confirm against a
    real export. Gold control columns come from GoldControlColumnsMixin."""

    __tablename__ = "Role"
    __table_args__ = {"schema": "gold"}

    RoleName: Mapped[str | None] = mapped_column("Role_Name", String(150))
    RoleType: Mapped[str | None] = mapped_column("Role_Type", String(50))
    RoleId: Mapped[int] = mapped_column("Role_Id", BigInteger, primary_key=True)
