from datetime import date

from sqlalchemy import BigInteger, Date, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import ClearOpsAuditColumnsMixin


class RateCard(ClearOpsAuditColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'ClearOps_RateCard'). Types are inferred from column names -- confirm against a
    real export. ClearOps-owned table (clearops schema); audit columns come from ClearOpsAuditColumnsMixin."""

    __tablename__ = "RateCard"
    __table_args__ = {"schema": "clearops"}

    ClientCode: Mapped[str | None] = mapped_column(String(255))
    GradeId: Mapped[int | None] = mapped_column("Grade_Id", BigInteger)
    Desciption: Mapped[str | None] = mapped_column(String(255))
    Rate: Mapped[float | None] = mapped_column(Numeric(18, 2))
    RateType: Mapped[str | None] = mapped_column(String(255))
    RateCardStartDate: Mapped[date | None] = mapped_column("Rate_Card_Start_Date", Date)
    RateCardEndDate: Mapped[date | None] = mapped_column("Rate_Card_End_Date", Date)
    TransactonCurrency: Mapped[str | None] = mapped_column("Transacton_Currency", String(255))
    RateCardId: Mapped[int] = mapped_column("Rate_Card_Id", BigInteger, primary_key=True)
    Country: Mapped[str | None] = mapped_column(String(150))
