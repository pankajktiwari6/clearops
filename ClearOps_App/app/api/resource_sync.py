"""Resource-level edits of the Strategic Time Planner grid (gold.ClearOps_ProjectSTP).

A resource can be staffed on several projects/tasks, so a rate edit must reach every
STP row of that resource, not only the row being edited in the grid. Rates live in
gold.ClearOps_RateCard (one resource-specific card, keyed by Desciption); every STP row
of the resource points at it through Rate_Card_Id and derives Monthly_Value from it.
"""
from datetime import datetime, timezone
from decimal import Decimal

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.project_stp import ProjectSTP
from app.models.rate_card import RateCard
from app.models.resource import Resource
from app.schemas.project_stp import ProjectSTPResponse


class ResourceRateUpdate(BaseModel):
    rate: float = Field(ge=0)


class ResourceHoursUpdate(BaseModel):
    task_id: int
    year_months: str = Field(description="Month key as stored in Year_Months, e.g. 'Oct 2026'")
    monthly_hours: float = Field(ge=0)


class ResourceSyncResponse(BaseModel):
    rate: float | None
    rows: list[ProjectSTPResponse]
    monthly_totals: dict[str, float]  # hours per Year_Months across every project the resource is on


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _value(hours, rate) -> float | None:
    return None if hours is None or rate is None else float(Decimal(str(hours)) * Decimal(str(rate)))


def _card_desc(resource_id: int) -> str:
    return f"Resource:{resource_id}"


def _totals(db: Session, resource_id: int) -> dict[str, float]:
    q = (select(ProjectSTP.YearMonths, func.sum(ProjectSTP.MonthlyHours))
         .where(ProjectSTP.ResorceId == resource_id).group_by(ProjectSTP.YearMonths))
    return {ym: float(h or 0) for ym, h in db.execute(q) if ym}


def _resource_card(db: Session, resource_id: int) -> RateCard | None:
    return db.scalars(select(RateCard).where(RateCard.Desciption == _card_desc(resource_id))).first()


def _require_resource(db: Session, resource_id: int) -> Resource:
    res = db.get(Resource, resource_id)
    if not res:
        raise HTTPException(404, "Resource not found")
    return res


def build_resource_sync_router() -> APIRouter:
    # Prefix stays under /clearops_projectstp so the gateway/domain routing is unchanged.
    router = APIRouter(prefix="/clearops_projectstp/resource", tags=["gold.ClearOps_ProjectSTP"])

    @router.put("/{resource_id}/rate", response_model=ResourceSyncResponse)
    def set_rate(resource_id: int, body: ResourceRateUpdate, db: Session = Depends(get_db),
                 x_user: str = Header("clearops-api")):
        """Set the resource's rate and re-price every STP row of that resource, in all projects."""
        res = _require_resource(db, resource_id)
        card = _resource_card(db, resource_id)
        if card is None:
            card = RateCard(Desciption=_card_desc(resource_id), GradeId=res.GradeId, RateType="Resource",
                            GoldCreatedBy=x_user)
            db.add(card)
        card.Rate = body.rate
        card.GoldModifiedBy, card.GoldModifiedDate = x_user, _now()
        db.flush()  # assigns Rate_Card_Id
        rows = db.scalars(select(ProjectSTP).where(ProjectSTP.ResorceId == resource_id)).all()
        for row in rows:
            row.RateCardId = card.RateCardId
            row.MonthlyValue = _value(row.MonthlyHours, body.rate)
            row.GoldModifiedBy, row.GoldModifiedDate = x_user, _now()
        db.commit()
        return ResourceSyncResponse(rate=body.rate, rows=rows, monthly_totals=_totals(db, resource_id))

    @router.put("/{resource_id}/hours", response_model=ResourceSyncResponse)
    def set_hours(resource_id: int, body: ResourceHoursUpdate, db: Session = Depends(get_db),
                  x_user: str = Header("clearops-api")):
        """Upsert one resource/task/month cell; Monthly_Value follows the resource's rate.

        The response carries the resource's per-month hours across all projects so every
        view of that resource (capacity tooltip, other project rows) can refresh.
        """
        _require_resource(db, resource_id)
        card = _resource_card(db, resource_id)
        row = db.scalars(select(ProjectSTP).where(
            ProjectSTP.ResorceId == resource_id, ProjectSTP.TaskId == body.task_id,
            ProjectSTP.YearMonths == body.year_months)).first()
        if row is None:
            row = ProjectSTP(ResorceId=resource_id, TaskId=body.task_id, YearMonths=body.year_months,
                             RateCardId=card.RateCardId if card else None, GoldCreatedBy=x_user)
            db.add(row)
        elif card is None and row.RateCardId:
            card = db.get(RateCard, row.RateCardId)
        row.MonthlyHours = body.monthly_hours
        row.MonthlyValue = _value(body.monthly_hours, card.Rate if card else None)
        row.GoldModifiedBy, row.GoldModifiedDate = x_user, _now()
        db.commit()
        db.refresh(row)
        return ResourceSyncResponse(rate=float(card.Rate) if card and card.Rate is not None else None,
                                    rows=[row], monthly_totals=_totals(db, resource_id))

    return router
