from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class Grade(GoldControlColumnsMixin, Base):
    """Mirrors gold.Grades in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    Source-data table, loaded by the pipeline. Audit/control columns come from GoldControlColumnsMixin."""

    __tablename__ = "Grades"
    __table_args__ = {"schema": "gold"}

    GradeId: Mapped[int] = mapped_column("Grade_Id", Integer, primary_key=True)
    JobCodeasgradeCode: Mapped[str] = mapped_column("Job_Codeasgrade_code", String(100))
    JobTitle: Mapped[str | None] = mapped_column("Job_title", String(200))
    BusinessTitle: Mapped[str | None] = mapped_column("Business_Title", String(200))
    Grade: Mapped[str | None] = mapped_column(String(100))
