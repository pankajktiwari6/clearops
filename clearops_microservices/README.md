# ClearOps Microservices

Implements the *Proposed ClearOps Technical Architecture* (Python 3.12 + FastAPI microservices on AKS,
MS SQL application DB, Azure Redis cache, Azure AD SSO, Azure Monitor, ADF/Functions + ADLS medallion pipeline)
over the table design in `Updated_ClearOps_Database_Final_fields.xlsx`.

```
React/TS web app --SSO--> Azure AD
        |  Bearer token
   gateway :8000  (validates Azure AD JWT, Redis read-cache, routes by domain)
        |  /api/<domain>/<table>[/<key>]
  +-----+-----------+---------------+--------------+
  setup :8001   timeplanner :8002   project :8003   admin :8004
  +-----+-----------+---------------+--------------+
                MS SQL  (gold / silver schemas)   <-- ADF + Azure Functions <-- ADLS landing <-- Oracle Fusion / Salesforce / Workday
```

| Service | Tables (mapping keys) |
|---|---|
| setup | Resource, LOB, Grade, FXRate, RateCard, Holiday, Passthrough, Employee |
| timeplanner | ProjectTimePlanner, Team, TimeOff, **WorkdayEmployeeTimeOff** |
| project | Project, ProjectWBS, ProjectEstimator, ProjectSTP, **ProjectSTPSetting**, SalesforceOpportunity, **OTLTimecard**, **ProjectTimecard** |
| admin | AdminIntegrationStatus, Role, User, Page, Access, Permission, Login, Log, UserLogin |

Bold = added from the updated design sheet (plus `Holiday.Holiday_month`).

**Code layout.** The ORM models, schemas and the mapping-driven CRUD live once in `../ClearOps_App/app`
(`column_mapping.json` is the source of truth). Each domain service is a 3-line `services/<domain>/service.py`
calling `create_app(title, tables)`, so adding a table = update the mapping/model/schema and list it in one domain.
All services share one database; each owns the API for its tables.

## Run locally
    cd clearops_microservices
    docker compose up --build            # mssql, redis, db-init (dev schema), 4 services, gateway
    curl localhost:8000/api/setup/lob

## Test
    pip install -r services/gateway/requirements.txt -r ../ClearOps_App/requirements.txt pytest
    pytest

## Deploy
`../.github/workflows/microservices.yml`: test -> build/push images to ACR -> `kubectl apply k8s/services.yaml` on AKS.
Secrets (DB URL, Redis URL, AAD ids, App Insights) come from Azure Key Vault via the CSI driver (`k8s/secrets-provider.yaml`).
Required GitHub config: vars `ACR_LOGIN_SERVER`, `AKS_RESOURCE_GROUP`, `AKS_CLUSTER`; secrets `AZURE_CLIENT_ID/TENANT_ID/SUBSCRIPTION_ID` (OIDC).

## Data pipeline
`data_pipeline/` has Azure Function stubs (`ingest`, `promote`) and a placeholder Bronze/Silver/Gold DDL. The real layer DDL is the
v2.8 design the ORM models mirror; replace the placeholder procs with it. `services/common/init_db.py` is dev-only table creation.

## Open questions on the updated sheet (not applied)
- `RateCard`: sheet lists `Job_title(FK)`, `Job_Code`, `Rate_schedule_Name`; the model keys rate cards by `Grade_Id`.
- `Grades.Job_Code` (model has `Job_Codeasgrade_code`), `Project_Master.Rate_Schedule_Id`, `Salesforce_Opportunity.LOB_ID(FK)`, `ClearOps_UserLogin.login`.
- `*_Sno` surrogate keys on Project_Master / ProjectWBS / Employee_Master / Salesforce_Opportunity (model uses `*_Id` / `Row_Id` / `SK`).
- Types for new columns (e.g. `Holiday_month` as text, `Month` as a date) are assumptions.
