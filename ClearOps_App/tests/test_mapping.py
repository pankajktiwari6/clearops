"""column_mapping.json must stay in lock-step with the ORM models and schemas."""
import importlib
import typing

import pytest
from sqlalchemy import inspect

from app.api.crud import MAPPING

TABLES = list(MAPPING.items())


def _model(name, spec):
    return getattr(importlib.import_module(spec["orm_module"]), name)


def _schemas(spec):
    return importlib.import_module(spec["api_schema_module"])


def test_all_expected_tables_present():
    assert len(MAPPING) == 25
    assert {"Project", "Employee", "SalesforceOpportunity", "FXRate", "ProjectWBS"} <= set(MAPPING)


@pytest.mark.parametrize("name,spec", TABLES, ids=[n for n, _ in TABLES])
def test_model_columns_match_mapping(name, spec):
    model = _model(name, spec)
    mapper = inspect(model)
    assert model.__table__.name == spec["table"]
    assert model.__table__.schema == spec["schema"]
    for col in spec["columns"]:
        attr = mapper.attrs[col["orm_attribute"]]
        db_col = attr.columns[0]
        assert db_col.name == col["db_column"]
        assert db_col.primary_key == col["primary_key"]
        if not col["primary_key"]:
            assert db_col.nullable == col["nullable"], col["db_column"]


@pytest.mark.parametrize("name,spec", TABLES, ids=[n for n, _ in TABLES])
def test_primary_key_matches_mapping(name, spec):
    pk = [c.name for c in _model(name, spec).__table__.primary_key.columns]
    assert pk == spec["primary_key"]


@pytest.mark.parametrize("name,spec", TABLES, ids=[n for n, _ in TABLES])
def test_response_schema_and_sort_fields_match_api_fields(name, spec):
    schemas = _schemas(spec)
    api_fields = [c["api_field"] for c in spec["columns"]]
    assert list(getattr(schemas, f"{name}Response").model_fields) == api_fields
    sort_fields = list(typing.get_args(getattr(schemas, f"{name}SortField")))
    assert set(sort_fields) <= set(api_fields)


@pytest.mark.parametrize("name,spec", TABLES, ids=[n for n, _ in TABLES])
def test_input_schemas_only_use_mapped_non_generated_fields(name, spec):
    schemas = _schemas(spec)
    generated = {c["api_field"] for c in spec["columns"] if c["server_generated"]}
    allowed = {c["api_field"] for c in spec["columns"]} - generated
    for kind in ("Create", "Update"):
        schema = getattr(schemas, f"{name}{kind}", None)
        if schema:
            assert set(schema.model_fields) <= allowed


def test_foreign_keys_in_mapping_exist_in_metadata():
    for name, spec in TABLES:
        table = _model(name, spec).__table__
        for col in spec["columns"]:
            if col["references"]:
                fks = {fk.target_fullname for fk in table.c[col["db_column"]].foreign_keys}
                assert col["references"] in fks


def test_source_tables_are_not_writable_except_app_edited_ones():
    for name in ("LOB", "Grade", "Employee", "Resource", "TimeOff", "ProjectWBS", "SalesforceOpportunity"):
        schemas = _schemas(MAPPING[name])
        assert not hasattr(schemas, f"{name}Create")
    for name in ("Project", "ProjectEstimator", "FXRate", "RateCard"):
        assert hasattr(_schemas(MAPPING[name]), f"{name}Create")
