"""Strategic Time Planner endpoints (saved queries, timeline/editability, resource propagation)."""
from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api import stp_logic as logic
from app.core.database import get_db
from app.models.project import Project
from app.models.project_stp import ProjectSTP
from app.models.project_stp_setting import ProjectSTPSetting
from app.models.project_wbs import ProjectWBS
from app.models.rate_card import RateCard
from app.models.user import User
from app.models.resource import Resource
from app.schemas.project_stp_setting import ProjectSTPSettingResponse

router = APIRouter(prefix="/stp", tags=["stp"])


def today() -> date:  # indirection so tests can pin the date
    return date.today()


def _windows(db: Session, project_ids: list[int]) -> list[logic.ProjectWindow]:
    rows = {p.ProjectId: p for p in db.scalars(select(Project).where(Project.ProjectId.in_(project_ids)))}
    missing = sorted(set(project_ids) - set(rows))
    if missing:
        raise HTTPException(404, f"Unknown project ids: {missing}")
    return [
        logic.ProjectWindow(i, logic.month_key(rows[i].ProjectEndDate) if rows[i].ProjectEndDate else None)
        for i in dict.fromkeys(project_ids)
    ]


class TimelineRequest(BaseModel):
    project_ids: list[int] = Field(min_length=1)


@router.post("/timeline")
def timeline(body: TimelineRequest, db: Session = Depends(get_db)):
    """Months to display (current .. max end month) and per-project editable months / rate editability."""
    return logic.build_timeline(_windows(db, body.project_ids), today())


def current_user(db: Session = Depends(get_db), x_user_email: str = Header("")) -> User:
    """The logged-in ClearOps user. The gateway sets x-user-email from the validated SSO token."""
    email = x_user_email.strip().lower()
    if not email:
        raise HTTPException(401, "Not signed in")
    user = db.scalars(select(User).where(func.lower(User.Email) == email)).first()
    if not user:
        raise HTTPException(403, f"No ClearOps user for {email}")
    return user


def _own_setting(db: Session, setting_id: int, user: User) -> ProjectSTPSetting:
    row = db.get(ProjectSTPSetting, setting_id)
    if not row or row.UserId != user.UserID:  # other users' queries look nonexistent
        raise HTTPException(404, "Not found")
    return row


# ---- saved queries -------------------------------------------------------------------------------------------

class SaveQueryRequest(BaseModel):
    filter_name: str = Field(min_length=1, max_length=200)
    project_ids: list[int] = Field(min_length=1)


@router.get("/settings", response_model=list[ProjectSTPSettingResponse])
def list_queries(db: Session = Depends(get_db), user: User = Depends(current_user)):
    """The logged-in user's saved queries, for the dropdown next to Save."""
    return db.scalars(
        select(ProjectSTPSetting).where(ProjectSTPSetting.UserId == user.UserID).order_by(ProjectSTPSetting.FilterName)
    ).all()


@router.post("/settings", response_model=ProjectSTPSettingResponse)
def save_query(body: SaveQueryRequest, db: Session = Depends(get_db), user: User = Depends(current_user)):
    """Save (or overwrite, same login + name) the current project selection."""
    x_user = user.Email or "clearops-api"
    ids = list(dict.fromkeys(body.project_ids))
    projects = {p.ProjectId: p for p in db.scalars(select(Project).where(Project.ProjectId.in_(ids)))}
    missing = sorted(set(ids) - set(projects))
    if missing:
        raise HTTPException(404, f"Unknown project ids: {missing}")
    name = body.filter_name.strip()
    if not name:
        raise HTTPException(422, "filter_name must not be blank")
    selected = {
        str(i): {"project_number": projects[i].ProjectNumber, "project_name": projects[i].ProjectName,
                 "project_end_date": projects[i].ProjectEndDate.isoformat() if projects[i].ProjectEndDate else None}
        for i in ids
    }
    row = db.scalars(select(ProjectSTPSetting).where(
        ProjectSTPSetting.UserId == user.UserID, ProjectSTPSetting.FilterName == name)).first()
    if row:
        row.ProjectIds, row.SelectedProjects = ids, selected
        row.GoldModifiedBy, row.GoldModifiedDate = x_user, datetime.now(timezone.utc).replace(tzinfo=None)
    else:
        row = ProjectSTPSetting(UserId=user.UserID, FilterName=name, ProjectIds=ids, SelectedProjects=selected,
                                GoldCreatedBy=x_user)
        db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get("/settings/{setting_id}/apply")
def apply_query(setting_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    """Selecting a saved query filters the grid to its projects (and returns their timeline)."""
    row = _own_setting(db, setting_id, user)
    return {"project_ids": row.ProjectIds, **logic.build_timeline(_windows(db, row.ProjectIds), today())}


@router.delete("/settings/{setting_id}", status_code=204)
def delete_query(setting_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    row = _own_setting(db, setting_id, user)
    db.delete(row)
    db.commit()


# ---- resource propagation ------------------------------------------------------------------------------------

def _allocations(db: Session, resource_id: int) -> list[logic.Allocation]:
    q = (select(ProjectSTP, ProjectWBS.ProjectId).join(ProjectWBS, ProjectWBS.ProjectWBSId == ProjectSTP.TaskId)
         .where(ProjectSTP.ResorceId == resource_id))
    return [
        logic.Allocation(resource_id, pid, r.YearMonths, float(r.MonthlyHours or 0), float(r.MonthlyValue or 0))
        for r, pid in db.execute(q)
    ]


def _refresh(db: Session, resource_id: int, project_id: int, year_month: str) -> dict:
    allocs = _allocations(db, resource_id)
    res = db.get(Resource, resource_id)
    return {
        "tooltip": logic.resource_month_summary(
            allocs, resource_id, year_month, project_id, res.WeeklyHours if res else None),
        # Every project this resource is tagged on, so the UI can refresh all tooltips and totals at once.
        "project_totals": logic.project_totals(allocs),
        "projects_affected": sorted({a.project_id for a in allocs}),
    }


@router.get("/resources/{resource_id}/summary")
def resource_summary(resource_id: int, year_month: str, project_id: int, db: Session = Depends(get_db)):
    return _refresh(db, resource_id, project_id, year_month)


class CellUpdate(BaseModel):
    resource_id: int
    task_id: int  # ProjectWBS.Project_WBS_Id the resource row sits under
    year_month: str = Field(pattern=r"^\d{4}-(0[1-9]|1[0-2])$")
    hours: float = Field(ge=0)
    rate: float | None = Field(default=None, ge=0)


@router.put("/cell")
def update_cell(body: CellUpdate, db: Session = Depends(get_db), x_user: str = Header("clearops-api")):
    """Save one forecast cell, enforce the project end date, and return every figure derived from this resource."""
    wbs = db.get(ProjectWBS, body.task_id)
    if not wbs:
        raise HTTPException(404, "Unknown task")
    window = _windows(db, [wbs.ProjectId])[0]
    if not logic.is_month_editable(window, body.year_month, today()):
        raise HTTPException(422, f"{body.year_month} is outside the editable window "
                                 f"(current month .. {window.end_month or 'no end date'})")
    row = db.scalars(select(ProjectSTP).where(
        ProjectSTP.ResorceId == body.resource_id, ProjectSTP.TaskId == body.task_id,
        ProjectSTP.YearMonths == body.year_month)).first()
    if not row:
        row = ProjectSTP(ResorceId=body.resource_id, TaskId=body.task_id, YearMonths=body.year_month,
                         TaskStartDate=date(int(body.year_month[:4]), int(body.year_month[5:]), 1),
                         GoldCreatedBy=x_user)
        db.add(row)
    rate = body.rate
    if rate is None and row.RateCardId:
        rc = db.get(RateCard, row.RateCardId)
        rate = float(rc.Rate) if rc and rc.Rate is not None else None
    row.MonthlyHours = body.hours
    row.MonthlyValue = round(body.hours * rate, 2) if rate is not None else row.MonthlyValue
    if row.ProjectSTPId:
        row.GoldModifiedBy, row.GoldModifiedDate = x_user, datetime.now(timezone.utc).replace(tzinfo=None)
    db.commit()
    return _refresh(db, body.resource_id, wbs.ProjectId, body.year_month)
