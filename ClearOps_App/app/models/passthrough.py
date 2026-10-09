from datetime import date

from sqlalchemy import BigInteger, Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldAuditColumnsMixin


class Passthrough(GoldAuditColumnsMixin, Base):
    """Mirrors gold.ClearOps_Passthrough in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    ClearOps application-owned table. Audit/control columns come from GoldAuditColumnsMixin."""

    __tablename__ = "ClearOps_Passthrough"
    __table_args__ = {"schema": "gold"}

    PassThroughId: Mapped[int] = mapped_column("Pass_Through_Id", BigInteger, primary_key=True)
    ContractNumber: Mapped[str | None] = mapped_column(String(450))
    ProjectID: Mapped[int | None] = mapped_column("Project_ID", BigInteger, ForeignKey("gold.Project_Master.Project_Id"))
    TransactionId: Mapped[int | None] = mapped_column(BigInteger)
    SupplierEmployeeName: Mapped[str | None] = mapped_column("Supplier_EmployeeName", String(450))
    SupplierInvoiceNumber: Mapped[str | None] = mapped_column(String(200))
    ExpenditureItemDate: Mapped[date | None] = mapped_column(Date)
    TransactionRowCost: Mapped[float | None] = mapped_column(Numeric(18, 2))
    TransactionCurrency: Mapped[str | None] = mapped_column(String(10))
