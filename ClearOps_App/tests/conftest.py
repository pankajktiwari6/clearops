import os
from datetime import datetime

os.environ.setdefault("DB_SERVER", "test")
os.environ.setdefault("DB_DATABASE", "test")
os.environ.setdefault("KEY_VAULT_URL", "https://test.vault.azure.net/")
os.environ["USE_KEYVAULT"] = "false"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import BigInteger, Cast, create_engine, event
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.crud import MAPPING
from app.core.database import Base, get_db
from app.main import app


# SQLite stand-ins for the SQL Server specifics the models rely on.
@compiles(BigInteger, "sqlite")
def _bigint_as_integer(type_, compiler, **kw):
    return "INTEGER"  # lets BIGINT identity keys auto-increment


@compiles(Cast, "sqlite")
def _drop_cast(element, compiler, **kw):
    inner = compiler.process(element.clause, **kw)
    return f"date({inner})"  # CAST(.. AS DATE) would yield an int in SQLite


def _load_all_models() -> None:
    import importlib

    for spec in MAPPING.values():
        importlib.import_module(spec["orm_module"])


@pytest.fixture()
def engine():
    _load_all_models()
    eng = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})

    @event.listens_for(eng, "connect")
    def _setup(dbapi_conn, _):
        dbapi_conn.create_function("sysutcdatetime", 0, lambda: datetime(2026, 10, 9, 12, 0, 0).isoformat(" "))
        for schema in ("gold", "silver"):
            dbapi_conn.execute(f"ATTACH DATABASE ':memory:' AS {schema}")

    Base.metadata.create_all(eng)
    yield eng
    eng.dispose()


@pytest.fixture()
def db(engine):
    with sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)() as session:
        yield session


@pytest.fixture()
def client(engine):
    maker = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    def _get_db():
        with maker() as session:
            yield session

    app.dependency_overrides[get_db] = _get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
