from datetime import date

from sqlalchemy import BigInteger, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldAuditColumnsMixin


class RateCard(GoldAuditColumnsMixin, Base):
    """Mirrors gold.ClearOps_RateCard in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    ClearOps application-owned table. Audit/control columns come from GoldAuditColumnsMixin."""

    __tablename__ = "ClearOps_RateCard"
    __table_args__ = {"schema": "gold"}

    RateCardId: Mapped[int] = mapped_column("Rate_Card_Id", BigInteger, primary_key=True)
    ClientCode: Mapped[str | None] = mapped_column(String(50))
    GradeId: Mapped[int | None] = mapped_column("Grade_Id", Integer, ForeignKey("gold.Grades.Grade_Id"))
    Desciption: Mapped[str | None] = mapped_column(String(500))
    Rate: Mapped[float | None] = mapped_column(Numeric(18, 4))
    RateType: Mapped[str | None] = mapped_column(String(50))
    RateCardStartDate: Mapped[date | None] = mapped_column("Rate_Card_Start_Date", Date)
    RateCardEndDate: Mapped[date | None] = mapped_column("Rate_Card_End_Date", Date)
    TransactonCurrency: Mapped[str | None] = mapped_column("Transacton_Currency", String(10))
    Country: Mapped[str | None] = mapped_column(String(100))
