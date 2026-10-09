import uuid

from app.models.fx_rate import FXRate
from app.models.lob import LOB
from app.models.project import Project

FX = "/api/clearops_fxrates"


def _fx(client, **over):
    body = {"source_funding_currency": "USD", "target_currency": "EUR", "rate": 0.92, **over}
    return client.post(FX, json=body)


def test_health_and_mapping_endpoint(client):
    assert client.get("/health").json() == {"status": "ok"}
    mapping = client.get("/api/column-mapping").json()
    assert "Project" in mapping and mapping["Project"]["table"] == "Project_Master"


def test_create_get_list_roundtrip(client, db):
    r = _fx(client)
    assert r.status_code == 201
    body = r.json()
    assert body["fx_rate_id"] == 1 and body["target_currency"] == "EUR"
    assert body["is_deleted"] is False and body["is_user_modified"] is False
    assert client.get(f"{FX}/1").json() == body
    assert [x["fx_rate_id"] for x in client.get(FX).json()] == [1]
    row = db.get(FXRate, 1)
    assert row.GoldCreatedBy == "clearops-api" and row.GoldCreatedDate is not None


def test_x_user_header_is_recorded_as_creator(client, db):
    client.post(FX, json={"source_funding_currency": "USD", "target_currency": "GBP"}, headers={"X-User": "pankaj"})
    assert db.get(FXRate, 1).GoldCreatedBy == "pankaj"


def test_create_requires_not_null_fields(client):
    r = client.post(FX, json={"rate": 1})
    assert r.status_code == 422
    missing = {e["loc"][-1] for e in r.json()["detail"]}
    assert missing == {"source_funding_currency", "target_currency"}


def test_patch_updates_only_sent_fields_and_stamps_modifier(client, db):
    _fx(client)
    r = client.patch(f"{FX}/1", json={"rate": 1.5}, headers={"X-User": "editor"})
    assert r.status_code == 200
    assert r.json()["rate"] == 1.5 and r.json()["source_funding_currency"] == "USD"
    row = db.get(FXRate, 1)
    assert row.GoldModifiedBy == "editor" and row.GoldModifiedDate is not None


def test_get_patch_delete_missing_row_404(client):
    assert client.get(f"{FX}/99").status_code == 404
    assert client.patch(f"{FX}/99", json={"rate": 1}).status_code == 404
    assert client.delete(f"{FX}/99").status_code == 404


def test_delete_removes_row(client):
    _fx(client)
    assert client.delete(f"{FX}/1").status_code == 204
    assert client.get(f"{FX}/1").status_code == 404


def test_list_sorting_and_paging(client):
    for cur, rate in (("EUR", 3), ("GBP", 1), ("JPY", 2)):
        _fx(client, target_currency=cur, rate=rate)
    rates = lambda **p: [x["rate"] for x in client.get(FX, params=p).json()]
    assert rates(sort_by="rate") == [1, 2, 3]
    assert rates(sort_by="rate", descending=True) == [3, 2, 1]
    assert rates(sort_by="rate", limit=1, offset=1) == [2]
    assert client.get(FX, params={"sort_by": "bogus"}).status_code == 422
    assert client.get(FX, params={"limit": 0}).status_code == 422


def test_source_tables_are_read_only(client):
    paths = client.get("/openapi.json").json()["paths"]
    assert set(paths["/api/lob"]) == {"get"}
    assert set(paths["/api/employee_master"]) == {"get"}
    assert "delete" not in paths["/api/project_master/{key}"]   # editable, but never deletable
    assert {"patch", "get"} <= set(paths["/api/project_master/{key}"])
    assert "delete" in paths[f"{FX}/{{key}}"]


def test_read_only_table_reads_seeded_rows(client, db):
    db.add(LOB(LOBName="Oncology", SourceRowHash=b"x", PipelineRunId=uuid.uuid4(), GoldCreatedBy="seed"))
    db.commit()
    body = client.get("/api/lob").json()
    assert body[0]["lob_name"] == "Oncology" and body[0]["lob_id"] == 1


def test_project_create_fills_pipeline_columns_and_maps_fields(client, db):
    r = client.post("/api/project_master", json={"project_number": "P-100", "project_name": "Alpha", "budget": 10.5})
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["project_number"] == "P-100" and body["project_name"] == "Alpha" and body["budget"] == 10.5
    row = db.get(Project, body["project_id"])
    assert row.ProjectName == "Alpha"                       # api field -> ORM attribute
    assert len(row.SourceRowHash) == 32 and isinstance(row.PipelineRunId, uuid.UUID)
    assert row.GoldCreatedBy == "clearops-api"


def test_project_requires_project_number(client):
    assert client.post("/api/project_master", json={"project_name": "x"}).status_code == 422
