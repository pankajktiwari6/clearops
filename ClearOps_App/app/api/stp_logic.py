"""Pure Strategic Time Planner (STP) rules -- no DB, no FastAPI, so they are trivially testable.

* Display months: current month .. latest end month of the selected projects.
* Editing: a project's rate and monthly forecast cells are editable current month .. its own end month.
* Resource totals: one resource tagged on several projects is summed per month so every tooltip and
  project-level total is derived from the same rows (single source of truth).
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date

DEFAULT_HORIZON_MONTHS = 12  # used when no selected project has an end date
WEEKS_PER_YEAR = 52


def month_key(d: date) -> str:
    return f"{d.year:04d}-{d.month:02d}"


def add_months(key: str, n: int) -> str:
    y, m = int(key[:4]), int(key[5:7])
    idx = y * 12 + (m - 1) + n
    return f"{idx // 12:04d}-{idx % 12 + 1:02d}"


def month_range(start: str, end: str) -> list[str]:
    """Inclusive list of 'YYYY-MM' keys; always at least `start` (an ended project still shows the current month)."""
    out, cur = [], start
    while cur <= end:
        out.append(cur)
        cur = add_months(cur, 1)
    return out or [start]


@dataclass(frozen=True)
class ProjectWindow:
    project_id: int
    end_month: str | None  # None = project has no end date


def display_months(projects: list[ProjectWindow], today: date) -> list[str]:
    """Current month .. max end month across the selected projects (not just the first / last picked)."""
    now = month_key(today)
    ends = [p.end_month for p in projects if p.end_month]
    return month_range(now, max(ends) if ends else add_months(now, DEFAULT_HORIZON_MONTHS - 1))


def editable_months(project: ProjectWindow, months: list[str], today: date) -> list[str]:
    """Months of the shared grid in which this project's rate / forecast cells accept input."""
    now = month_key(today)
    return [m for m in months if m >= now and (project.end_month is None or m <= project.end_month)]


def is_month_editable(project: ProjectWindow, year_month: str, today: date) -> bool:
    return year_month in editable_months(project, [year_month], today)


def build_timeline(projects: list[ProjectWindow], today: date) -> dict:
    months = display_months(projects, today)
    out = []
    for p in projects:
        ed = editable_months(p, months, today)
        out.append({
            "project_id": p.project_id,
            "end_month": p.end_month,
            "rate_editable": bool(ed),  # rate can only change while the project is still running
            "editable_months": ed,
        })
    return {"months": months, "projects": out}


def monthly_capacity(weekly_hours: float | None) -> float | None:
    return None if weekly_hours is None else round(float(weekly_hours) * WEEKS_PER_YEAR / 12, 2)


@dataclass(frozen=True)
class Allocation:
    resource_id: int
    project_id: int
    year_month: str
    hours: float
    value: float = 0.0


def resource_month_summary(
    allocations: list[Allocation], resource_id: int, year_month: str, project_id: int, weekly_hours: float | None
) -> dict:
    """Tooltip payload for one resource/month: this project vs other projects vs remaining capacity."""
    this = other = 0.0
    for a in allocations:
        if a.resource_id == resource_id and a.year_month == year_month:
            if a.project_id == project_id:
                this += a.hours
            else:
                other += a.hours
    cap = monthly_capacity(weekly_hours)
    remaining = None if cap is None else round(cap - this - other, 2)
    return {
        "resource_id": resource_id,
        "year_month": year_month,
        "capacity_hours": cap,
        "this_project_hours": round(this, 2),
        "other_projects_hours": round(other, 2),
        "remaining_hours": remaining,
        "remaining_pct": None if not cap else round(remaining / cap * 100, 1),
        "over_allocated": remaining is not None and remaining < 0,
    }


def project_totals(allocations: list[Allocation]) -> dict[int, dict[str, dict[str, float]]]:
    """{project_id: {year_month: {hours, value}, 'total': {hours, value}}} recomputed from raw rows."""
    acc: dict[int, dict[str, dict[str, float]]] = defaultdict(lambda: defaultdict(lambda: {"hours": 0.0, "value": 0.0}))
    for a in allocations:
        for key in (a.year_month, "total"):
            acc[a.project_id][key]["hours"] += a.hours
            acc[a.project_id][key]["value"] += a.value
    return {
        p: {k: {"hours": round(v["hours"], 2), "value": round(v["value"], 2)} for k, v in months.items()}
        for p, months in acc.items()
    }
