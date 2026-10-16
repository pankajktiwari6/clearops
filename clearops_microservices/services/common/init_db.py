"""Dev only: create the gold/silver schemas and tables in a fresh database.

Production schemas are owned by the Bronze/Silver/Gold DDL and the ADF pipelines.
"""
import time

from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.api.crud import MAPPING
import importlib

from app.core.database import Base, engine

for spec in MAPPING.values():
    importlib.import_module(spec["orm_module"])

for attempt in range(30):
    try:
        with engine.begin() as conn:
            for schema in ("gold", "silver"):
                conn.execute(text(f"IF SCHEMA_ID('{schema}') IS NULL EXEC('CREATE SCHEMA {schema}')"))
        break
    except OperationalError:
        time.sleep(2)
else:
    raise SystemExit("database not reachable")

Base.metadata.create_all(engine)
print("schema ready")
