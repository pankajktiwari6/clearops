# STP – End-to-End Implementation

How every STP feature flows from the screen to the database and back, with the steps to deploy and verify it.
Companion to `docs/STP.md` (requirements, API, frontend prompt).

## 1. Architecture
```
Browser (STP page) ──SSO bearer token──► API gateway ──► project service (FastAPI) ──► SQL Server (gold.*)
                                          │ validates Azure AD token                 │ ClearOps_App/app/api/stp.py
                                          │ adds x-user-email from the token         │ + stp_logic.py (pure rules)
                                          └ proxies /api/project/stp/... → /api/stp/...
```
| Layer | File | Responsibility |
|---|---|---|
| Gateway | `clearops_microservices/services/gateway/gateway/main.py` | validate token, forward `x-user-email` (client value never trusted) |
| Endpoints | `ClearOps_App/app/api/stp.py` | timeline, saved queries, cell save, resource summary |
| Rules | `ClearOps_App/app/api/stp_logic.py` | month window, editability, capacity, totals (no DB, unit-tested) |
| Model/schema | `app/models|schemas/project_stp_setting.py`, `column_mapping.json` | `stp_settings` table |
| Service wiring | `services/project/service.py` | `ProjectSTPSetting` added to the project domain |
| Tests | `clearops_microservices/tests/test_stp.py` | 19 tests incl. end-to-end API flows on SQLite |

## 2. Database
Create once (SQL Server). `DateOfData` etc. come from the Gold audit mixin.
```sql
CREATE TABLE gold.ClearOps_STPSettings (
  STP_Setting_Id    BIGINT IDENTITY PRIMARY KEY,
  User_Id           BIGINT        NOT NULL REFERENCES gold.ClearOps_Users(User_ID),
  Filter_Name       VARCHAR(200)  NOT NULL,
  Project_Ids       NVARCHAR(MAX) NOT NULL,   -- JSON list of Project_Master.Project_Id
  Selected_Projects NVARCHAR(MAX) NULL,       -- JSON object {id:{project_number,project_name,project_end_date}}
  Date_Time         DATETIME NULL DEFAULT SYSUTCDATETIME(),
  DateOfData        DATE NULL DEFAULT CAST(SYSUTCDATETIME() AS DATE),
  GoldCreatedBy     VARCHAR(100) NOT NULL,
  GoldCreatedDate   DATETIME NOT NULL DEFAULT SYSUTCDATETIME(),
  GoldModifiedBy    VARCHAR(100) NULL,
  GoldModifiedDate  DATETIME NULL,
  CONSTRAINT UQ_STPSettings_User_Filter UNIQUE (User_Id, Filter_Name)
);
```
Prerequisites: each login email exists in `gold.ClearOps_Users.Email`; `Project_Master.Project_End_Date`,
`Resources.WeeklyHours` and `ClearOps_ProjectSTP` (Year_Months as `YYYY-MM`, Task_Id → `ProjectWBS`) are populated.

## 3. Flows

### A. Open page / select projects
1. User selects projects → UI `POST /stp/timeline {project_ids}`.
2. Service reads `Project_End_Date` per project → `build_timeline`: months = current → max end month;
   per project `editable_months` (current → its end) and `rate_editable`.
3. UI renders those columns and disables rate/hours inputs outside each project's `editable_months`.
   No saved query is needed – this is the default path.

### B. Save a query
1. Select ≥ 1 project → **Save Query** enabled → modal (Enter Query Name) → Save.
2. `POST /stp/settings {filter_name, project_ids}`; gateway adds `x-user-email`; service resolves the user
   (401/403 otherwise), validates the projects, upserts on (user, name) and stores `Project_Ids` +
   `Selected_Projects`.
3. UI refreshes the dropdown from `GET /stp/settings` (own queries only).

### C. Apply a query
Dropdown selection → `GET /stp/settings/{id}/apply` → UI sets the project selector to `project_ids` and loads
the grid with the returned timeline. "No saved query" keeps manual selection untouched.

### D. Edit hours (resource propagation + capacity)
1. User types hours for resource R in project A, month M → store updated optimistically, input capped at
   `capacity − other_projects_hours`.
2. `PUT /stp/cell {resource_id, task_id, year_month, hours, rate?}`.
3. Service: task → project; reject 422 if M is outside current…project end; upsert the `ClearOps_ProjectSTP`
   row (value = hours × rate); recompute R's allocations over **all** projects; reject 422 (rollback) if the
   total exceeds capacity (working days × ≤ 8 h) and hours increased; otherwise commit.
4. Response `{tooltip, project_totals, projects_affected}` → UI refreshes tooltips and totals of every project
   where R is tagged, from one shared store.

## 4. Deploy checklist
1. Run the DDL above (or `Base.metadata.create_all` in a non-prod DB).
2. Deploy the gateway and project service; set `AAD_TENANT_ID`, `AAD_CLIENT_ID`, `AUTH_ENABLED=true`
   (`DEV_USER_EMAIL` only for local dev with auth off).
3. Build the frontend using Part C of `docs/STP.md`.

## 5. Verification
* Backend: `cd clearops_microservices && python -m pytest tests -q` (needs `pip install -r
  ClearOps_App/requirements.txt pytest httpx redis pyjwt`).
* Manual UAT:
  - [ ] P1 only → columns end at P1's end month; P1 cells locked after it.
  - [ ] P1+P2+P3 → columns end at the max end month; each project locks at its own end month.
  - [ ] Save Query disabled with no project; save "My Q" → appears in dropdown for me, not for another user.
  - [ ] Select "My Q" → projects filter; choose none → manual selection still shows data.
  - [ ] Edit R's hours in P1 → tooltip/totals in P2 update without reload.
  - [ ] Entering hours beyond (working days × 8 − other-project hours) is blocked client- and server-side.
  - [ ] Editing a month after the project end date is rejected.

## 6. Known limits
Holidays and time off are not deducted from capacity; the 12-month default applies only when no selected
project has an end date; the frontend is not part of this repository.
