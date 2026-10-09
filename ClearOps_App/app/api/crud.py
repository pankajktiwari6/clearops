"""Generic, mapping-driven REST routers.

One router per entry in column_mapping.json: list (paging + server-side sort),
get by key, and -- where the schema module defines Create/Update -- create,
update and (ClearOps-owned tables only) delete. API field names are mapped to
ORM attributes via the same JSON the frontend uses.
"""
import hashlib
import importlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, get_args

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db

MAPPING = json.loads((Path(__file__).resolve().parent.parent / "column_mapping.json").read_text())["tables"]


def _build(name: str, spec: dict) -> APIRouter:
    model = getattr(importlib.import_module(spec["orm_module"]), name)
    schemas = importlib.import_module(spec["api_schema_module"])
    response = getattr(schemas, f"{name}Response")
    create = getattr(schemas, f"{name}Create", None)
    update = getattr(schemas, f"{name}Update", None)
    sort_fields = get_args(getattr(schemas, f"{name}SortField"))
    to_attr = {c["api_field"]: c["orm_attribute"] for c in spec["columns"]}
    pk_attr = to_attr[next(c["api_field"] for c in spec["columns"] if c["primary_key"])]
    pk_type = next(c["python_type"] for c in spec["columns"] if c["primary_key"])
    pk_py = {"int": int, "str": str}[pk_type]
    source = spec["mixin"] != "GoldAuditColumnsMixin"
    router = APIRouter(prefix=f"/{spec['table'].lower()}", tags=[f"{spec['schema']}.{spec['table']}"])

    def stamp_create(row: Any, user: str) -> None:
        for col, val in (("GoldCreatedBy", user), ("SilverCreatedBy", user)):
            if hasattr(row, col):
                setattr(row, col, val)
        if hasattr(row, "PipelineRunId"):
            row.PipelineRunId = uuid.uuid4()
        if hasattr(row, "SourceRowHash"):
            row.SourceRowHash = hashlib.sha256(repr(sorted(
                (k, repr(v)) for k, v in vars(row).items() if not k.startswith("_"))).encode()).digest()

    @router.get("", response_model=list[response])
    def list_rows(
        db: Session = Depends(get_db),
        limit: int = Query(100, ge=1, le=1000),
        offset: int = Query(0, ge=0),
        sort_by: str | None = Query(None, description=f"One of: {', '.join(sort_fields)}"),
        descending: bool = False,
    ):
        stmt = select(model)
        col = getattr(model, pk_attr)
        if sort_by:
            if sort_by not in sort_fields:
                raise HTTPException(422, f"sort_by must be one of {list(sort_fields)}")
            col = getattr(model, to_attr[sort_by])
        stmt = stmt.order_by(col.desc() if descending else col).offset(offset).limit(limit)
        return db.scalars(stmt).all()

    @router.get("/{key}", response_model=response)
    def get_row(key: pk_py, db: Session = Depends(get_db)):  # type: ignore[valid-type]
        row = db.get(model, key)
        if not row:
            raise HTTPException(404, "Not found")
        return row

    if create:
        @router.post("", response_model=response, status_code=201)
        def create_row(body: create, db: Session = Depends(get_db), x_user: str = Header("clearops-api")):  # type: ignore[valid-type]
            row = model(**{to_attr[k]: v for k, v in body.model_dump().items()})
            stamp_create(row, x_user)
            db.add(row)
            db.commit()
            db.refresh(row)
            return row

    if update:
        @router.patch("/{key}", response_model=response)
        def update_row(key: pk_py, body: update, db: Session = Depends(get_db), x_user: str = Header("clearops-api")):  # type: ignore[valid-type]
            row = db.get(model, key)
            if not row:
                raise HTTPException(404, "Not found")
            for k, v in body.model_dump(exclude_unset=True).items():
                setattr(row, to_attr[k], v)
            if hasattr(row, "GoldModifiedBy"):
                row.GoldModifiedBy, row.GoldModifiedDate = x_user, datetime.now(timezone.utc).replace(tzinfo=None)
            db.commit()
            db.refresh(row)
            return row

    if create and not source:
        @router.delete("/{key}", status_code=204)
        def delete_row(key: pk_py, db: Session = Depends(get_db)):  # type: ignore[valid-type]
            row = db.get(model, key)
            if not row:
                raise HTTPException(404, "Not found")
            db.delete(row)
            db.commit()

    return router


def build_routers() -> list[APIRouter]:
    return [_build(name, spec) for name, spec in MAPPING.items()]
