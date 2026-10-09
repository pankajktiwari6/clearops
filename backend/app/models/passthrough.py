from datetime import date

from sqlalchemy import BigInteger, Date, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class Passthrough(GoldControlColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'ClearOps_Passthrough'). Types are inferred from column names -- confirm against a
    real export. Gold control columns come from GoldControlColumnsMixin."""

    __tablename__ = "Passthrough"
    __table_args__ = {"schema": "gold"}

    ContractNumber: Mapped[str | None] = mapped_column(String(255))
    ProjectID: Mapped[int | None] = mapped_column("Project_ID", BigInteger)
    TransactionId: Mapped[int | None] = mapped_column(BigInteger)
    SupplierEmployeeName: Mapped[str | None] = mapped_column("Supplier/EmployeeName", String(150))
    SupplierInvoiceNumber: Mapped[str | None] = mapped_column(String(255))
    ExpenditureItemDate: Mapped[date | None] = mapped_column(Date)
    TransactionRowCost: Mapped[float | None] = mapped_column(Numeric(18, 2))
    TransactionCurrency: Mapped[str | None] = mapped_column(String(255))
    PassThroughId: Mapped[int] = mapped_column("Pass_Through_Id", BigInteger, primary_key=True)
