from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import BigInteger, create_engine, event
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api import stp, stp_logic as L
from app.core.database import Base, get_db
from app.main import create_app

@compiles(BigInteger, "sqlite")
def _bigint_as_integer(*_, **__):  # so BIGINT primary keys autoincrement under SQLite
    return "INTEGER"


TODAY = date(2026, 10, 25)
P1, P2, P3 = L.ProjectWindow(1, "2027-06"), L.ProjectWindow(2, "2028-08"), L.ProjectWindow(3, "2027-12")


def test_scenario_1_single_project():
    t = L.build_timeline([P1], TODAY)
    assert t["months"][0] == "2026-10" and t["months"][-1] == "2027-06"
    assert t["projects"][0]["editable_months"] == t["months"]


def test_scenario_2_two_projects():
    t = L.build_timeline([P1, P2], TODAY)
    assert t["months"][-1] == "2028-08"
    assert t["projects"][0]["editable_months"][-1] == "2027-06"
    assert t["projects"][1]["editable_months"][-1] == "2028-08"


def test_scenario_3_three_projects():
    t = L.build_timeline([P1, P2, P3], TODAY)
    assert t["months"][-1] == "2028-08"
    assert [p["editable_months"][-1] for p in t["projects"]] == ["2027-06", "2028-08", "2027-12"]
    assert "2027-07" not in t["projects"][0]["editable_months"]


def test_ended_project_and_missing_end_date():
    ended = L.ProjectWindow(9, "2026-01")
    t = L.build_timeline([ended], TODAY)
    assert t["months"] == ["2026-10"] and not t["projects"][0]["rate_editable"]
    assert len(L.display_months([L.ProjectWindow(8, None)], TODAY)) == 12


def test_resource_summary_sums_across_projects():
    a = [L.Allocation(5, 1, "2026-11", 20, 2400), L.Allocation(5, 2, "2026-11", 40, 4800),
         L.Allocation(5, 2, "2026-12", 10, 1200)]
    s = L.resource_month_summary(a, 5, "2026-11", 1, 40)
    assert (s["this_project_hours"], s["other_projects_hours"]) == (20, 40)
    assert s["remaining_hours"] == round(40 * 52 / 12 - 60, 2)
    assert L.project_totals(a)[2]["total"] == {"hours": 50, "value": 6000}


@pytest.fixture
def client(monkeypatch):
    engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})

    @event.listens_for(engine, "connect")
    def _setup(conn, _):
        for schema in ("gold", "silver"):
            conn.execute(f"ATTACH ':memory:' AS {schema}")
        conn.create_function("sysutcdatetime", 0, lambda: "2026-10-25 00:00:00")

    for spec in __import__("app.api.crud", fromlist=["MAPPING"]).MAPPING.values():
        __import__(spec["orm_module"])
    for table in Base.metadata.tables.values():  # CAST(.. AS DATE) is not meaningful under SQLite
        if "DateOfData" in table.c:
            table.c.DateOfData.server_default = None
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    app = create_app()

    def db():
        with Session() as s:
            yield s

    app.dependency_overrides[get_db] = db
    monkeypatch.setattr(stp, "today", lambda: TODAY)
    with Session() as s:
        from app.models.project import Project
        from app.models.project_wbs import ProjectWBS
        from app.models.resource import Resource
        for pid, end in ((1, date(2027, 6, 30)), (2, date(2028, 8, 31))):
            s.add(Project(ProjectId=pid, ProjectNumber=f"P{pid}", ProjectName=f"Proj {pid}", ProjectEndDate=end,
                          GoldCreatedBy="t", SourceRowHash=b"x", PipelineRunId=__import__("uuid").uuid4()))
            s.add(ProjectWBS(ProjectWBSId=pid * 10, TaskNumber="1", ProjectId=pid, GoldCreatedBy="t",
                             SourceRowHash=b"x", PipelineRunId=__import__("uuid").uuid4()))
        s.add(Resource(ResourceID=5, HRID="h", WeeklyHours=40, GoldCreatedBy="t", SourceRowHash=b"x",
                       PipelineRunId=__import__("uuid").uuid4()))
        s.commit()
    return TestClient(app)


def test_timeline_endpoint(client):
    r = client.post("/api/stp/timeline", json={"project_ids": [1, 2]}).json()
    assert r["months"][-1] == "2028-08" and r["projects"][0]["editable_months"][-1] == "2027-06"
    assert client.post("/api/stp/timeline", json={"project_ids": [99]}).status_code == 404


def test_saved_query_lifecycle(client):
    body = {"user_id": 7, "filter_name": "My Q", "project_ids": [1, 2]}
    first = client.post("/api/stp/settings", json=body).json()
    assert first["project_ids"] == [1, 2] and first["selected_projects"]["1"]["project_number"] == "P1"
    again = client.post("/api/stp/settings", json={**body, "project_ids": [2]}).json()
    assert again["stp_setting_id"] == first["stp_setting_id"] and again["project_ids"] == [2]
    assert [q["filter_name"] for q in client.get("/api/stp/settings?user_id=7").json()] == ["My Q"]
    assert client.get("/api/stp/settings?user_id=8").json() == []
    applied = client.get(f"/api/stp/settings/{first['stp_setting_id']}/apply").json()
    assert applied["project_ids"] == [2] and applied["months"][-1] == "2028-08"
    assert client.delete(f"/api/stp/settings/{first['stp_setting_id']}").status_code == 204


def test_cell_update_propagates_and_enforces_end_date(client):
    put = lambda task, ym, h: client.put("/api/stp/cell", json={
        "resource_id": 5, "task_id": task, "year_month": ym, "hours": h, "rate": 100})
    assert put(10, "2026-11", 20).status_code == 200
    r = put(20, "2026-11", 40).json()
    assert r["projects_affected"] == [1, 2]
    assert r["tooltip"]["this_project_hours"] == 40 and r["tooltip"]["other_projects_hours"] == 20
    r = put(10, "2026-11", 30).json()  # edit on project 1 -> project 2's view reflects it
    assert client.get("/api/stp/resources/5/summary?year_month=2026-11&project_id=2").json()["tooltip"]["other_projects_hours"] == 30
    assert r["project_totals"]["1"]["total"] == {"hours": 30, "value": 3000}
    assert put(10, "2027-07", 5).status_code == 422  # after project 1 end date
    assert put(20, "2027-07", 5).status_code == 200  # project 2 still running
    assert put(10, "2026-09", 5).status_code == 422  # past month
