from datetime import date

from sqlalchemy import BigInteger, Date, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import GoldControlColumnsMixin


class Employee(GoldControlColumnsMixin, Base):
    """Columns taken from ClearOps_Database_Final_DB_Tables.xlsx (sheet
    'Employee_Master'). Types are inferred from column names -- confirm against a
    real export. Source-data table (gold schema); control columns come from GoldControlColumnsMixin."""

    __tablename__ = "Employee"
    __table_args__ = {"schema": "gold"}

    RowId: Mapped[int | None] = mapped_column("Row_Id", BigInteger)
    HRID: Mapped[str] = mapped_column(String(50), primary_key=True)
    PreferredFirstName: Mapped[str | None] = mapped_column("Preferred_first_name", String(150))
    LastName: Mapped[str | None] = mapped_column("Last_name", String(150))
    ContinuousServiceDate: Mapped[date | None] = mapped_column("Continuous_Service_Date", Date)
    FirstStartDate: Mapped[date | None] = mapped_column("First_Start_Date", Date)
    LastStartDate: Mapped[date | None] = mapped_column("Last_Start_Date", Date)
    ExpectedEndDate: Mapped[date | None] = mapped_column("Expected_End_Date", Date)
    JobCode: Mapped[str | None] = mapped_column("Job_Code", String(255))
    JobTitle: Mapped[str | None] = mapped_column("Job_title", String(150))
    BusinessTitle: Mapped[str | None] = mapped_column(String(150))
    GradeID: Mapped[int | None] = mapped_column("Grade_ID", BigInteger)
    JobEntryDate: Mapped[date | None] = mapped_column("Job_Entry_Date", Date)
    LineOfBusiness: Mapped[str | None] = mapped_column("Line_Of_Business", String(255))
    LineOfBusinessCode: Mapped[str | None] = mapped_column("Line_of_Business_code", String(255))
    Country: Mapped[str | None] = mapped_column(String(150))
    RegTemp: Mapped[str | None] = mapped_column("Reg_Temp", String(255))
    FullPart: Mapped[str | None] = mapped_column("Full_Part", String(255))
    FTE: Mapped[float | None] = mapped_column("Fte", Numeric(4, 2))
    Region: Mapped[str | None] = mapped_column(String(50))
    Email: Mapped[str | None] = mapped_column(String(255))
    ScheduledWeeklyHours: Mapped[float | None] = mapped_column("Scheduled_Weekly_Hours", Numeric(18, 2))
    LOBID: Mapped[int | None] = mapped_column("LOB_ID", BigInteger)
    ProjectId: Mapped[int | None] = mapped_column("Project_Id", BigInteger)
