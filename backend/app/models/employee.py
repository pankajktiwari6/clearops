from datetime import date

from sqlalchemy import BigInteger, Boolean, Date, FetchedValue, ForeignKey, Integer, LargeBinary, Numeric, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class Employee(GoldControlColumnsMixin, Base):
    """Mirrors gold.Employee_Master in ClearOps_Stage_Bronze_Silver_Gold_Database_Design (v2.8).
    Source-data table, loaded by the pipeline. Audit/control columns come from GoldControlColumnsMixin."""

    __tablename__ = "Employee_Master"
    __table_args__ = {"schema": "gold"}

    RowId: Mapped[int] = mapped_column("Row_Id", BigInteger, unique=True)
    HRID: Mapped[str] = mapped_column(String(100), primary_key=True)
    PreferredFirstName: Mapped[str | None] = mapped_column("Preferred_first_name", String(200))
    LastName: Mapped[str | None] = mapped_column("Last_name", String(200))
    ContinuousServiceDate: Mapped[date | None] = mapped_column("Continuous_Service_Date", Date)
    FirstStartDate: Mapped[date | None] = mapped_column("First_Start_Date", Date)
    LastStartDate: Mapped[date | None] = mapped_column("Last_Start_Date", Date)
    ExpectedEndDate: Mapped[str | None] = mapped_column("Expected_End_Date", String(50))
    JobCode: Mapped[str | None] = mapped_column("Job_Code", String(100))
    JobTitle: Mapped[str | None] = mapped_column("Job_title", String(200))
    BusinessTitle: Mapped[str | None] = mapped_column(String(200))
    GradeID: Mapped[int | None] = mapped_column("Grade_ID", Integer, ForeignKey("gold.Grades.Grade_Id"))
    JobEntryDate: Mapped[date | None] = mapped_column("Job_Entry_Date", Date)
    LineOfBusiness: Mapped[str | None] = mapped_column("Line_Of_Business", String(120))
    LineOfBusinessCode: Mapped[str | None] = mapped_column("Line_of_Business_code", String(100))
    Country: Mapped[str | None] = mapped_column(String(100))
    RegTemp: Mapped[str | None] = mapped_column("Reg_Temp", String(100))
    FullPart: Mapped[str | None] = mapped_column("Full_Part", String(100))
    FTE: Mapped[float | None] = mapped_column("Fte", Numeric(5, 2))
    Region: Mapped[str | None] = mapped_column(String(100))
    Email: Mapped[str | None] = mapped_column(String(320))
    ScheduledWeeklyHours: Mapped[float | None] = mapped_column("Scheduled_Weekly_Hours", Numeric(6, 2))
    RowVersion: Mapped[bytes | None] = mapped_column(LargeBinary, server_default=FetchedValue(), server_onupdate=FetchedValue())
    IsDeleted: Mapped[bool] = mapped_column(Boolean, server_default=text("0"))
    SourceSystem: Mapped[str] = mapped_column(String(50), server_default=text("'Workday'"))
    IsUserModified: Mapped[bool] = mapped_column(Boolean, server_default=text("0"))
    LOBID: Mapped[int | None] = mapped_column("LOB_ID", Integer, ForeignKey("gold.LOB.LOB_Id"))
    ProjectId: Mapped[int | None] = mapped_column("Project_Id", BigInteger, ForeignKey("gold.Project_Master.Project_Id"))
