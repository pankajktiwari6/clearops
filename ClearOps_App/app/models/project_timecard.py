from datetime import date, datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Identity, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class ProjectTimecard(GoldControlColumnsMixin, Base):
    """gold.Project_Timecard: Oracle project timecard transactions. Added from Updated_ClearOps_Database_Final_fields.xlsx.
    Source-data table, loaded by the pipeline. Audit/control columns come from GoldControlColumnsMixin."""

    __tablename__ = "Project_Timecard"
    __table_args__ = {"schema": "gold"}

    ProjectTimecardSno: Mapped[int] = mapped_column("Project_Timecard_Sno", BigInteger, Identity())
    TRANSACTIONID: Mapped[int] = mapped_column("TRANSACTION_ID", BigInteger, primary_key=True, autoincrement=False)
    PROJECTNUM: Mapped[str | None] = mapped_column("PROJECT_NUM", String(100))
    TASKNUMBER: Mapped[str | None] = mapped_column("TASK_NUMBER", String(100))
    TIMEENTRYDATE: Mapped[date] = mapped_column("TIME_ENTRY_DATE", Date)
    EMPLOYEENUMBER: Mapped[str | None] = mapped_column("EMPLOYEE_NUMBER", String(100))
    TASKNAME: Mapped[str | None] = mapped_column("TASK_NAME", String(450))
    HOURSTYPE: Mapped[str | None] = mapped_column("HOURS_TYPE", String(100))
    HOURS: Mapped[float | None] = mapped_column(Numeric(8, 2))
    PERIOD: Mapped[str | None] = mapped_column(String(50))
    COMMENTS: Mapped[str | None] = mapped_column(String(1000))
    LastUpdateDate: Mapped[datetime | None] = mapped_column("last_update_date", DateTime)
    LastProcessedDate: Mapped[datetime | None] = mapped_column("last_processed_date", DateTime)
    DlLastProcessedDate: Mapped[datetime | None] = mapped_column("dl_last_processed_date", DateTime)
    SourceModifiedDate: Mapped[datetime | None] = mapped_column(DateTime)
    LoadBatchId: Mapped[str | None] = mapped_column(String(100))
    StageInsertedTimestamp: Mapped[datetime | None] = mapped_column(DateTime)
    IsProcessed: Mapped[bool | None] = mapped_column(Boolean)
