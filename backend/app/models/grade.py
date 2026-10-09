from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class Grade(GoldControlColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'Grades'). Types are inferred from column names -- confirm against a
    real export. Source-data table (gold schema); control columns come from GoldControlColumnsMixin."""

    __tablename__ = "Grade"
    __table_args__ = {"schema": "gold"}

    JobCode: Mapped[str | None] = mapped_column("Job_Code", String(255))
    JobTitle: Mapped[str | None] = mapped_column("Job_title", String(150))
    BusinessTitle: Mapped[str | None] = mapped_column("Business_Title", String(150))
    GradeId: Mapped[int] = mapped_column("Grade_Id", BigInteger, primary_key=True)
    Grade: Mapped[str | None] = mapped_column(String(255))
