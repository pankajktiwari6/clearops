from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Date, DateTime, LargeBinary, String, Uuid, cast, func
from sqlalchemy.orm import Mapped, mapped_column


class GoldAuditColumnsMixin:
    """DateOfData + the four Gold audit columns (ClearOps application-owned tables)."""

    DateOfData: Mapped[date | None] = mapped_column(Date, server_default=cast(func.sysutcdatetime(), Date))
    GoldCreatedBy: Mapped[str] = mapped_column(String(100))
    GoldCreatedDate: Mapped[datetime] = mapped_column(DateTime, server_default=func.sysutcdatetime())
    GoldModifiedBy: Mapped[str | None] = mapped_column(String(100))
    GoldModifiedDate: Mapped[datetime | None] = mapped_column(DateTime)


class GoldControlColumnsMixin(GoldAuditColumnsMixin):
    """Audit columns plus pipeline lineage (Silver-fed Gold tables)."""

    SourceRowHash: Mapped[bytes] = mapped_column(LargeBinary(32))
    PipelineRunId: Mapped[UUID] = mapped_column(Uuid)


class SilverControlColumnsMixin:
    """Control columns of silver.SalesforceOpportunity."""

    SourceRowHash: Mapped[bytes] = mapped_column(LargeBinary(32))
    SourceModifiedDate: Mapped[datetime | None] = mapped_column(DateTime)
    DateOfData: Mapped[date] = mapped_column(Date)
    PipelineRunId: Mapped[UUID] = mapped_column(Uuid)
    IsDeleted: Mapped[bool] = mapped_column(server_default="0")
    SilverCreatedBy: Mapped[str] = mapped_column(String(100))
    SilverCreatedDate: Mapped[datetime] = mapped_column(DateTime, server_default=func.sysutcdatetime())
    SilverModifiedBy: Mapped[str | None] = mapped_column(String(100))
    SilverModifiedDate: Mapped[datetime | None] = mapped_column(DateTime)
