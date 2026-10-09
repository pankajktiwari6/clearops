from sqlalchemy import BigInteger, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class ProjectEstimator(GoldControlColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'ProjectEstimator'). Types are inferred from column names -- confirm against a
    real export. Source-data table (gold schema); control columns come from GoldControlColumnsMixin."""

    __tablename__ = "ProjectEstimator"
    __table_args__ = {"schema": "gold"}

    TaskID: Mapped[int | None] = mapped_column("Task_ID", BigInteger)
    ProjectEstimaterId: Mapped[int] = mapped_column("Project_Estimater_Id", BigInteger, primary_key=True)
    JobTitle: Mapped[str | None] = mapped_column("Job_title", String(150))
    TaskName: Mapped[str | None] = mapped_column("Task_Name", String(150))
    QTY: Mapped[float | None] = mapped_column(Numeric(18, 2))
    HRS: Mapped[float | None] = mapped_column(Numeric(18, 2))
    Rate: Mapped[float | None] = mapped_column(Numeric(18, 2))
    Total: Mapped[float | None] = mapped_column(Numeric(18, 2))
    SubTotal: Mapped[float | None] = mapped_column(Numeric(18, 2))
    TaskNumber: Mapped[str | None] = mapped_column("Task_Number", String(255))
    ProjectId: Mapped[int | None] = mapped_column("Project_Id", BigInteger)
    ParentTaskID: Mapped[int | None] = mapped_column("Parent_Task_ID", BigInteger)
    DeliveryType: Mapped[str | None] = mapped_column("Delivery_Type", String(255))
    ResourceId: Mapped[int | None] = mapped_column("Resource_Id", BigInteger)
