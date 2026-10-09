from sqlalchemy import Boolean, FetchedValue, Integer, LargeBinary, Numeric, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldAuditColumnsMixin


class FXRate(GoldAuditColumnsMixin, Base):
    """Mirrors gold.ClearOps_FXRates in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    ClearOps application-owned table. Audit/control columns come from GoldAuditColumnsMixin."""

    __tablename__ = "ClearOps_FXRates"
    __table_args__ = {"schema": "gold"}

    FXRateId: Mapped[int] = mapped_column("FX_Rate_Id", Integer, primary_key=True)
    SourceFundingCurrency: Mapped[str] = mapped_column(String(10))
    TargetCurrency: Mapped[str] = mapped_column(String(10))
    Rate: Mapped[float | None] = mapped_column(Numeric(18, 8))
    RowVersion: Mapped[bytes | None] = mapped_column(LargeBinary, server_default=FetchedValue(), server_onupdate=FetchedValue())
    IsDeleted: Mapped[bool] = mapped_column(Boolean, server_default=text("0"))
    SourceSystem: Mapped[str | None] = mapped_column(String(50))
    IsUserModified: Mapped[bool] = mapped_column(Boolean, server_default=text("0"))
    Status: Mapped[str | None] = mapped_column(String(30))
