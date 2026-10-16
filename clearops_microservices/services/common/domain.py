"""Builds one domain microservice: the ClearOps_App model/CRUD layer restricted to the tables the domain owns."""
from app.main import create_app

from .telemetry import setup_telemetry


def make_service(title: str, tables: set[str]):
    setup_telemetry()
    return create_app(title, tables)
