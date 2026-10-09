from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class LOB(GoldControlColumnsMixin, Base):
    """Mirrors gold.LOB in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    Source-data table, loaded by the pipeline. Audit/control columns come from GoldControlColumnsMixin."""

    __tablename__ = "LOB"
    __table_args__ = {"schema": "gold"}

    LOBId: Mapped[int] = mapped_column("LOB_Id", Integer, primary_key=True)
    LOBName: Mapped[str] = mapped_column(String(450))
    Entity: Mapped[str | None] = mapped_column(String(450))
    Status: Mapped[str | None] = mapped_column(String(30))
    LineOfBusinessGl: Mapped[str | None] = mapped_column("Line_Of_Business_Gl", String(450))
    BusinessUnit: Mapped[str | None] = mapped_column("Business_Unit", String(450))
