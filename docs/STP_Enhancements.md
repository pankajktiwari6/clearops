# Strategic Time Planner (STP) – End-Date Window, Saved Queries, Resource Propagation

> Scope: this repo contains the FastAPI backend only. The endpoints below return everything the STP grid
> needs (months, editable flags, tooltip values, totals); the React/UI wiring is described per section.

## 1. Display months and editable window (end date)

Rules (`ClearOps_App/app/api/stp_logic.py`):

| Item | Rule |
|---|---|
| Displayed months | current month → **max** `Project_End_Date` month of all selected projects |
| Rate card + monthly forecast cells (per project) | editable current month → that project's own end month; later months are read-only |
| Rate card editable | only while the project has not ended |
| Project has no end date | editable throughout; if *no* selected project has one, a 12-month horizon is shown |
| All selected projects already ended | the current month is still shown, all cells read-only |

Example (today = Oct 2026; P1 ends Jun 2027, P2 Aug 2028, P3 Dec 2027):

| Selection | Months shown | P1 editable | P2 editable | P3 editable |
|---|---|---|---|---|
| P1 | Oct 2026 – Jun 2027 | → Jun 2027 | – | – |
| P1, P2 | Oct 2026 – Aug 2028 | → Jun 2027 | → Aug 2028 | – |
| P1, P2, P3 | Oct 2026 – Aug 2028 | → Jun 2027 | → Aug 2028 | → Dec 2027 |

`POST /api/stp/timeline` `{ "project_ids": [1,2] }` →
```json
{ "months": ["2026-10", "..."],
  "projects": [{ "project_id": 1, "end_month": "2027-06", "rate_editable": true,
                 "editable_months": ["2026-10", "..."] }] }
```
UI: call it whenever the project selection changes; render `months` as columns and disable an input when
its month is not in that project's `editable_months` (and the rate input when `rate_editable` is false).
The server re-validates on save (`PUT /api/stp/cell` → 422 outside the window).

## 2. Saved queries (STP settings)

Table `gold.ClearOps_STPSettings` (model `ProjectSTPSetting`, mapped in `column_mapping.json`):

| Column | Type | Notes |
|---|---|---|
| `STP_Setting_Id` | BIGINT identity PK | |
| `User_Id` | BIGINT FK `gold.ClearOps_Users.User_ID` | logged-in user |
| `Filter_Name` | NVARCHAR(200) | unique per user (`UQ_STPSettings_User_Filter`) |
| `Project_Ids` | JSON | list of `Project_Master.Project_Id` |
| `Selected_Projects` | JSON | `{ "<id>": {project_number, project_name, project_end_date} }` |
| `Date_Time` + Gold audit columns | | |

### Identity comes from the login
The client never sends a user id. The gateway validates the Azure AD (SSO) token and forwards the user's
email as `x-user-email` (claims `email` → `preferred_username` → `upn`; any client-supplied value is dropped;
with `AUTH_ENABLED=false` it uses `DEV_USER_EMAIL`). The project service resolves it to
`gold.ClearOps_Users.User_ID` (case-insensitive `Email`) and:
* no email → **401**; email with no ClearOps user → **403**;
* `User_Id` of a saved query is always the logged-in user; list/apply/delete only see **own** queries
  (someone else's id → 404); the same name under another login is a separate query.
* Existing behaviour checked: before this change the gateway validated the token but forwarded no identity and
  the table's `user_id` would have had to be sent by the client – now removed from the request body and the
  query string.

UI flow
1. **Save Query** button next to Save – disabled until ≥ 1 project is selected.
2. Click → modal with one text box (**Enter Query Name**), **Save** and **Cancel**.
3. Save → `POST /api/stp/settings` `{filter_name, project_ids}`; re-using a name overwrites that query.
4. The dropdown next to Save is filled from `GET /api/stp/settings`.
5. Choosing a query → `GET /api/stp/settings/{id}/apply` returns `project_ids` (+ timeline) – set the project
   filter to them. Not choosing one leaves the existing behaviour untouched. `DELETE /api/stp/settings/{id}` removes one.

Generic CRUD for the table is also exposed at `/api/clearops_stpsettings` (project service).

## 3. Resource propagation (tooltip + calculations)

A resource can be tagged on several projects. Every figure is derived from the same `ClearOps_ProjectSTP`
rows (joined to `ProjectWBS.Project_Id`), so nothing is stored twice and nothing goes stale:

* Tooltip per resource/month: `capacity` (= `Resources.WeeklyHours × 52 / 12`), **this project** hours,
  **other projects** hours, **remaining** hours and % (negative ⇒ `over_allocated`).
* Project totals (hours and value per month and in total) are recomputed from the rows.

`PUT /api/stp/cell` `{resource_id, task_id, year_month, hours, rate?}` saves the cell (value = hours × rate;
rate falls back to the row's rate card) and returns, in one response:
```json
{ "tooltip": {"this_project_hours": 40, "other_projects_hours": 20, "remaining_hours": 113.33, "...": "..."},
  "project_totals": {"1": {"2026-11": {"hours": 20, "value": 2000}, "total": {"hours": 20, "value": 2000}},
                     "2": { "...": "..." }},
  "projects_affected": [1, 2] }
```
UI: after each save, replace the tooltip data and project totals for **every** project in
`projects_affected` (every row where that resource appears) from this response. `GET
/api/stp/resources/{id}/summary?year_month=&project_id=` returns the same payload for hover refreshes.

## 4. Files
`app/models|schemas/project_stp_setting.py`, `app/api/stp_logic.py` (pure rules), `app/api/stp.py` (endpoints),
`column_mapping.json`, project microservice `TABLES`, tests in `clearops_microservices/tests/test_stp.py`.
Create the new table with `CREATE TABLE gold.ClearOps_STPSettings …` from the model (or `Base.metadata.create_all`).
