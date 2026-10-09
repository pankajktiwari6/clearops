from sqlalchemy import BigInteger, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class ProjectEstimator(GoldControlColumnsMixin, Base):
    """Mirrors gold.ProjectEstimator in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    Source-data table, loaded by the pipeline. Audit/control columns come from GoldControlColumnsMixin."""

    __tablename__ = "ProjectEstimator"
    __table_args__ = {"schema": "gold"}

    ProjectEstimaterId: Mapped[int] = mapped_column("Project_Estimater_Id", BigInteger, primary_key=True)
    TaskID: Mapped[int | None] = mapped_column("Task_ID", BigInteger, ForeignKey("gold.ProjectWBS.Project_WBS_Id"))
    JobTitle: Mapped[str | None] = mapped_column("Job_title", String(200))
    TaskName: Mapped[str | None] = mapped_column("Task_Name", String(500))
    QTY: Mapped[float | None] = mapped_column(Numeric(18, 4))
    HRS: Mapped[float | None] = mapped_column(Numeric(18, 4))
    Rate: Mapped[float | None] = mapped_column(Numeric(18, 4))
    Total: Mapped[float | None] = mapped_column(Numeric(18, 2))
    SubTotal: Mapped[float | None] = mapped_column(Numeric(18, 2))
    TaskNumber: Mapped[str | None] = mapped_column("Task_Number", String(124))
    ProjectId: Mapped[int | None] = mapped_column("Project_Id", BigInteger, ForeignKey("gold.Project_Master.Project_Id"))
    ParentTaskID: Mapped[int | None] = mapped_column("Parent_Task_ID", BigInteger, ForeignKey("gold.ProjectWBS.Project_WBS_Id"))
    DeliveryType: Mapped[str | None] = mapped_column("Delivery_Type", String(100))
    ResourceId: Mapped[int | None] = mapped_column("Resource_Id", BigInteger, ForeignKey("gold.Resources.Resource_ID"))
