from sqlalchemy import BigInteger, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import ClearOpsAuditColumnsMixin


class FXRate(ClearOpsAuditColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'ClearOps_FXRates'). Types are inferred from column names -- confirm against a
    real export. ClearOps-owned table (clearops schema); audit columns come from ClearOpsAuditColumnsMixin."""

    __tablename__ = "FXRate"
    __table_args__ = {"schema": "clearops"}

    FXRateId: Mapped[int] = mapped_column("FX_Rate_Id", BigInteger, primary_key=True)
    SourceFundingCurrency: Mapped[str | None] = mapped_column(String(255))
    TargetCurrency: Mapped[str | None] = mapped_column(String(255))
    Rate: Mapped[float | None] = mapped_column(Numeric(18, 2))
    Status: Mapped[str | None] = mapped_column(String(50))
