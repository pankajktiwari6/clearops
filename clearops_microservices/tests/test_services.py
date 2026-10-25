import importlib.util
import pathlib

import pytest
from fastapi.testclient import TestClient

from app.api.crud import MAPPING

SERVICES = pathlib.Path(__file__).resolve().parents[1] / "services"
DOMAINS = ["setup", "timeplanner", "project", "admin"]


def load(domain: str):
    spec = importlib.util.spec_from_file_location(f"{domain}_service", SERVICES / domain / "service.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_domains_partition_every_mapped_table_exactly_once():
    owned = [t for d in DOMAINS for t in load(d).TABLES]
    assert sorted(owned) == sorted(MAPPING)


def test_new_tables_from_updated_design_are_mapped():
    assert {"WorkdayEmployeeTimeOff", "OTLTimecard", "ProjectTimecard"} <= set(MAPPING)
    assert "holiday_month" in [c["api_field"] for c in MAPPING["Holiday"]["columns"]]


@pytest.mark.parametrize("domain", DOMAINS)
def test_service_exposes_only_its_tables(domain):
    mod = load(domain)
    c = TestClient(mod.app)
    assert c.get("/health").json() == {"status": "ok"}
    paths = c.get("/openapi.json").json()["paths"]
    prefixes = {p.split("/")[2] for p in paths if p.startswith("/api/") and p != "/api/column-mapping"}
    prefixes.discard("stp")  # hand-written STP endpoints, served by the project service alongside ProjectSTP
    assert prefixes == {MAPPING[t]["table"].lower() for t in mod.TABLES}
    assert set(c.get("/api/column-mapping").json()) == mod.TABLES


def test_new_tables_compile_for_mssql():
    from sqlalchemy.dialects import mssql
    from sqlalchemy.schema import CreateTable

    from app.models.otl_timecard import OTLTimecard
    from app.models.project_timecard import ProjectTimecard
    from app.models.workday_employee_time_off import WorkdayEmployeeTimeOff

    for model in (OTLTimecard, ProjectTimecard, WorkdayEmployeeTimeOff):
        assert "gold." in str(CreateTable(model.__table__).compile(dialect=mssql.dialect()))


def test_gateway_requires_azure_ad_token():
    from gateway import main as gw
    c = TestClient(gw.app)
    assert c.get("/health").status_code == 200
    assert c.get("/api/setup/lob").status_code == 401
    assert c.get("/api/setup/lob", headers={"authorization": "Bearer junk"}).status_code == 401


def test_gateway_routes_domain_to_service(monkeypatch):
    from gateway import auth, main as gw
    monkeypatch.setattr(auth, "AUTH_ENABLED", False)
    seen = {}

    class FakeClient:
        async def __aenter__(self): return self
        async def __aexit__(self, *a): return False

        async def request(self, method, url, **kw):
            seen["url"] = url
            import httpx
            return httpx.Response(200, json=[], headers={"content-type": "application/json"})

    monkeypatch.setattr(gw.httpx, "AsyncClient", lambda **kw: FakeClient())
    c = TestClient(gw.app)
    assert c.get("/api/project/clearops_projectwbs/12").status_code == 200
    assert seen["url"] == f"{gw.ROUTES['project']}/api/clearops_projectwbs/12"
    assert c.get("/api/nope/x").status_code == 404
