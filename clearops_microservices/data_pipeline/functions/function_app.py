"""Azure Functions: extraction / injection / orchestration helpers called by Azure Data Factory."""
import json
import os

import azure.functions as func
import pyodbc

app = func.FunctionApp()


def _sql() -> pyodbc.Connection:
    return pyodbc.connect(os.environ["SQL_ODBC_CONNECTION"], autocommit=True)


@app.route(route="ingest/{source}/{entity}", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def ingest(req: func.HttpRequest) -> func.HttpResponse:
    """Store a raw API response (Oracle Fusion / Salesforce / Workday) in bronze."""
    source, entity = req.route_params["source"], req.route_params["entity"]
    payload = req.get_body().decode()
    json.loads(payload)  # reject malformed JSON
    with _sql() as conn:
        conn.execute("INSERT INTO bronze.raw_ingest (source, entity, payload) VALUES (?,?,?)",
                     source, entity, payload)
    return func.HttpResponse(status_code=202)


@app.route(route="promote", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def promote(req: func.HttpRequest) -> func.HttpResponse:
    """Bronze -> Silver -> Gold. ADF calls this after each extraction run."""
    with _sql() as conn:
        conn.execute("EXEC silver.usp_load_from_bronze")
        conn.execute("EXEC gold.usp_load_from_silver")
    return func.HttpResponse("promoted")
