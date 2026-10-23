# Prompt: STP saved queries + project end-date rules

Paste (or point Claude at) this file to implement the feature. Work on the current branch. Do not open a PR.

## Role and goal

You are working in the ClearOps repo. Implement per-user saved STP project queries in the backend, with a tested end-date rule module and a frontend contract doc. Prefer minimal, pattern-matching changes. Do not guess. Anything you cannot confirm from the code goes in the final "Unverified / assumptions" list.

## Business requirements (source of truth)

### End dates on the STP page
- Displayed months run from the current month to the **max end date of all selected projects**.
- Edit Rate Card and Monthly Forecast Value are enabled for a project **only from the current month through that project's own end date**.

Example: P1 ends Jun 2027, P2 ends Aug 2028, P3 ends Dec 2027.

| Selected | Months shown | Editable |
|---|---|---|
| P1 | now -> Jun 2027 | P1: now -> Jun 2027 |
| P1, P2 | now -> Aug 2028 | P1 -> Jun 2027; P2 -> Aug 2028 |
| P1, P2, P3 | now -> Aug 2028 | P1 -> Jun 2027; P2 -> Aug 2028; P3 -> Dec 2027 |

### Saved queries
1. A **Save Query** button on the STP screen, disabled until at least one project is selected.
2. Clicking it opens a popup with one text box ("Enter Query Name") and Save and Cancel buttons.
3. The user enters a name and clicks Save.
4. The name appears in a dropdown next to the Save Query button.
5. Selecting a saved query from the dropdown re-selects the saved projects (filters the selection).
6. **Toolbar and default view.** The STP toolbar, left to right, is: a **Projects** multi-select dropdown, a **Save Query** button, and a **Saved Queries** dropdown (placeholder text "Saved Queries" means no query is applied).
   - **Manual selection.** When no saved query is selected, the user can pick any projects from the Projects dropdown. The dropdown always lists every project the user can see.
   - **Viewing STP data.** As soon as the user selects one or more projects in the Projects dropdown, the grid shows the STP details (rows, months, rate card and monthly forecast values) for exactly those projects, and Save Query becomes enabled. This works the same whether or not a saved query is applied.
   - **No filter.** With no saved query and no manual selection, the grid shows **all** projects the user can see.
   - **Saved query.** Choosing one from Saved Queries fills the Projects dropdown with that query's projects and narrows the grid to them.
   - **Editing after applying a query.** If the user then changes the Projects selection by hand, the Saved Queries dropdown resets to its placeholder (the selection is now a manual one). The user can save it under a new name.
   - **Clearing.** Clearing the Projects selection returns to the all-projects view; Saved Queries resets to its placeholder.
   - With no filter, the visible set is all projects, so the month range runs from the current month to the max end date across all shown projects, and each project is editable only through its own end date (same rules as above).
   - There is no stored "All projects" row. The unfiltered view is a UI state, not a saved query.
   - Save Query stays disabled until the user has explicitly selected at least one project. Showing all projects by default does not count as a selection.
   - If the user's saved queries fail to load, the page still shows all projects.
7. Persist in an STP settings table: user id (from login), filter name, and a JSON list of selected project ids from the project table. After login, the STP dropdown loads that user's saved queries.

## Step 0: Verify before writing code (report briefly, then proceed)

Confirm by reading the files. If a fact is false, adapt and say so.

1. `ClearOps_App/app/api/crud.py` builds routers from `column_mapping.json`. It supports list, get, create, patch, and delete (delete only for non-source tables). It reads an `x_user` header, default `"clearops-api"`.
2. `ProjectSTP.TaskId` is an FK to `gold.ProjectWBS.Project_WBS_Id`, and `ProjectWBS.ProjectId` is an FK to `gold.Project_Master.Project_Id`. `Project_Master.Project_End_Date` is a nullable `Date`.
3. `ProjectSTP.YearMonths` is `String(20)`. Find in the repo or `docs/` what format it holds (for example `2027-06` or `Jun-2027`). If undeterminable, do not parse it in server code. Isolate parsing in one helper and list it as an assumption.
4. The gateway (`clearops_microservices/services/gateway/gateway/main.py`, `auth.py`) validates the Azure AD JWT but forwards only `content-type`, so downstream services never learn the caller. Check whether `ClearOps_Users` (`Email`, `HRID`) or `ClearOps_login` (`SSO`, `Email`, `HRID`) is the right place to resolve a token claim to `User_ID`. Pick one and justify it in one line.
5. Tests run with `DATABASE_URL=sqlite://` (`clearops_microservices/tests/conftest.py`). CI runs flake8 (`E9,F63,F7,F82` must be clean) and pytest.
6. `clearops_microservices/tests/test_services.py` requires every key in `MAPPING` to be owned by exactly one service's `TABLES`. `test_service_exposes_only_its_tables` compares service routes with `MAPPING`.

## Part A: Table `gold.ClearOps_STPSettings`

**Model** `ClearOps_App/app/models/stp_settings.py`, class `STPSettings(GoldAuditColumnsMixin, Base)`, with `__table_args__ = {"schema": "gold"}`:

| Attribute | DB column | Type | Notes |
|---|---|---|---|
| `STPSettingsId` | `STP_Settings_Id` | BigInteger | PK, identity |
| `UserId` | `User_ID` | BigInteger | FK -> `gold.ClearOps_Users.User_ID`, not null |
| `FilterName` | `Filter_Name` | String(200) | not null |
| `ProjectIds` | `Project_Ids` | JSON array of `Project_Master.Project_Id` | not null; a type that compiles on both SQLite and MSSQL |

- UniqueConstraint on (`User_ID`, `Filter_Name`); Index on `User_ID`.
- Docstring in the style of the other models.
- Production DDL is not generated by this repo. Write the T-SQL `CREATE TABLE` (with `ISJSON(Project_Ids)=1` check, FK, unique index) into `docs/stp-saved-queries.md`. `init_db.py` (`create_all`) is dev only.

**Schemas** `ClearOps_App/app/schemas/stp_settings.py`, following `schemas/project_stp.py` exactly (`Create`, `Update`, `Response` with `validation_alias`, `SortField` Literal):
- `filter_name` stripped, 1-200 chars.
- `project_ids` non-empty list of unique ints > 0, with a sensible maximum (state it).
- `Create` and `Update` must not accept `user_id`.

**Registration**
- Add an `STPSettings` entry to `column_mapping.json`, same keys and structure as `ProjectSTP`.
- Add it to `TABLES` in `clearops_microservices/services/project/service.py`.
- Update the README domain table.
- Per-user scoping cannot be expressed by the generic router, so give this table a dedicated router and exclude it from generic route generation without breaking the partition and route tests. Keep the URL shape (`/api/clearops_stpsettings`) consistent with the others.

**Endpoints (dedicated router)**

| Method | Behavior |
|---|---|
| `GET` | The caller's queries, sorted by name |
| `GET /{id}` | One of the caller's queries; another user's returns **404** |
| `POST` | `user_id` from the caller; **409** on duplicate name; **422** listing invalid ids if any id is not in `Project_Master` |
| `PATCH /{id}` | Rename or change ids, same validations |
| `DELETE /{id}` | Delete the caller's query; 204 |
| `GET /{id}/projects` | Saved ids resolved to `{project_id, project_name, project_end_date}`; ids that no longer exist are dropped and returned in `missing_ids` |

Concurrency: for simultaneous creates of the same name, rely on the DB unique constraint and map the integrity error to 409.

## Part B: Caller identity through the gateway

- After `authenticate`, resolve the caller from verified claims (`preferred_username`/`email`, never an unverified header) to `User_ID`. Forward it as an internal header (for example `X-ClearOps-User-Id`).
- Downstream services trust this header only from the gateway. Document how (network policy or a shared internal secret). **Strip any inbound header of that name at the gateway.**
- If the caller cannot be resolved to a ClearOps user, return 403 for the STP settings endpoints.
- Keep `AUTH_ENABLED=false` dev mode working: allow a dev-only override env var, default off.
- Gateway cache: the GET cache key ignores the caller today. Include the user id in the key, or bypass the cache for the STP settings paths. Add a test showing user A's cached list is never served to user B.

## Part C: End-date rules (pure module and tests)

Create `ClearOps_App/app/services/stp_dates.py` (or the closest existing home for helpers). Pure functions, no DB access:
- `visible_months(selected_projects, today)`: month starts from the month of `today` to the month of the max `end_date`.
- `editable_months(project, today)`: months from the month of `today` to the month of the project's `end_date`, inclusive.
- `is_editable(project, month, today)`.

Rules:
- Month granularity: compare `(year, month)`, never days. Inclusive end.
- Empty selection: the caller passes all visible projects when no filter is active (see "Toolbar and default view"), so `visible_months` is never called with an implicit empty "no filter" case. For a truly empty project list, return the current month only or an empty list (pick one and document it).
- An `end_date` before the current month gives just the current month, read-only.
- Null `end_date` means open-ended: editable through the displayed range, and it does not shorten the max.
- Inject `today`. Never call `date.today()` inside the logic.

Tests with `today = 2026-10-23`, P1 end = 2027-06-30, P2 = 2028-08-31, P3 = 2027-12-31: the three scenarios in the table above, plus boundary months (editable Jun 2027, not Jul 2027 for P1), null end date, past end date, empty selection, and a single-month range.

**Server-side guard on `ProjectSTP` create/update:** resolve the project through `task_id` -> `ProjectWBS.ProjectId` -> `Project_End_Date`. Reject with 422 when `year_months` falls after the project's end month. This depends on the `year_months` format check in Step 0. If the format is undeterminable, skip the guard and report it. Do not otherwise alter existing ProjectSTP behavior.

## Part D: Frontend contract (`docs/stp-saved-queries.md`)

The STP UI is not in this repo. Document precisely enough to implement without questions:
- Toolbar order: Projects multi-select, Save Query button, Saved Queries dropdown. Save Query is disabled until at least one project is selected in the Projects dropdown (either manually or from a saved query).
- Projects dropdown: always lists all projects the user can see. It is selectable whenever no saved query is applied, and also after one is applied (a manual change resets the Saved Queries dropdown to its placeholder).
- Modal: one input labelled "Enter Query Name", plus Save and Cancel. Save disabled for empty or whitespace-only names. A 409 shows an inline "name already exists" error. Cancel clears the input.
- Dropdown next to the button: loads on page load, refreshes after a save. Its placeholder state means no query is applied (the grid shows all projects, or the manual Projects selection). There is no stored "All projects" entry. If the list fails to load, the page still shows all projects.
- Month range and editable cells with no filter are computed over all shown projects, using the same rules as Part C.
- Selecting a saved query replaces the current selection, resolves ids via `/{id}/projects`, shows a notice for `missing_ids`, and recomputes months and editable cells.
- Endpoints: request and response JSON examples and error codes for all of them.
- The T-SQL DDL from Part A.

## Constraints and quality bar

- Match surrounding code style, naming and comment density. No new dependencies unless unavoidable.
- No change to unrelated tables or endpoints. Existing tests pass unchanged, except deliberate additions to the partition and route tests.
- Run `flake8 . --select=E9,F63,F7,F82` and `pytest` (from `clearops_microservices`) and paste the pass/fail summary. If something fails, fix the cause. Do not skip or weaken tests.
- Compile-check the new table for MSSQL, like `test_new_tables_compile_for_mssql`.
- Commit with a clear message on the current branch.

## Definition of done (all must be true)

1. New tests cover: per-user isolation; duplicate name -> 409; unknown project id -> 422; delete and rename; `/projects` with a stale id; gateway cache-key isolation; the three date scenarios and boundaries; MSSQL compile.
2. The partition and route tests pass.
3. The gateway ignores a client-supplied identity header.
4. The final message lists changes by file, the test output, and an **"Unverified / assumptions"** section (at least the `year_months` format, the identity-claim mapping, and the production DB).
