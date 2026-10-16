import importlib.util
import pathlib

from fastapi.testclient import TestClient

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load(service: str):
    spec = importlib.util.spec_from_file_location(f"{service}_main", ROOT / service / "app" / "main.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_user_crud():
    c = TestClient(load("user_service").app)
    r = c.post("/users", json={"name": "Ada", "email": "ada@example.com"})
    assert r.status_code == 201
    assert c.get(f"/users/{r.json()['id']}").json()["name"] == "Ada"
    assert c.get("/users/999").status_code == 404


def test_order_validates_user(monkeypatch):
    mod = load("order_service")
    monkeypatch.setattr(mod, "user_exists", lambda uid: uid == 1)
    c = TestClient(mod.app)
    assert c.post("/orders", json={"user_id": 1, "item": "pen", "quantity": 2}).status_code == 201
    assert c.post("/orders", json={"user_id": 2, "item": "pen", "quantity": 2}).status_code == 404
    assert c.post("/orders", json={"user_id": 1, "item": "pen", "quantity": 0}).status_code == 422


def test_gateway_unknown_service():
    c = TestClient(load("gateway").app)
    assert c.get("/health").status_code == 200
    assert c.get("/api/nope/x").status_code == 404
