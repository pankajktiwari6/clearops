from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class LOB(GoldControlColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'LOB'). Types are inferred from column names -- confirm against a
    real export. Gold control columns come from GoldControlColumnsMixin."""

    __tablename__ = "LOB"
    __table_args__ = {"schema": "gold"}

    LOBName: Mapped[str | None] = mapped_column(String(150))
    Entity: Mapped[str | None] = mapped_column(String(255))
    Status: Mapped[str | None] = mapped_column(String(50))
    LOBId: Mapped[int] = mapped_column("LOB_Id", BigInteger, primary_key=True)
    LineOfBusinessGl: Mapped[str | None] = mapped_column("Line_Of_Business_Gl", String(255))
    BusinessUnit: Mapped[str | None] = mapped_column("Business_Unit", String(255))
