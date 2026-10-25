# Strategic Time Planner (STP) – Complete Guide

One file covering requirements, backend design/API, and the frontend implementation prompt.
Backend lives in `ClearOps_App/app/api/stp.py` (endpoints) and `stp_logic.py` (pure rules); tests in
`clearops_microservices/tests/test_stp.py`. This repo has no frontend – Part C is the prompt for it.

---

## Part A – Requirements

1. **Month window by end date** – displayed months = current month → **latest** project end month among the
   selected projects. A project's rate card and monthly forecast cells are editable only from the current month
   to **that project's own** end month.
2. **Saved queries** – *Save Query* button (disabled until a project is selected) → popup with **Enter Query Name**,
   Save, Cancel → saved per logged-in user in `stp_settings` → shown in a dropdown next to Save → selecting one
   filters the grid to its projects. If no saved query is selected, existing functionality stays in place: the user
   selects projects from the project drop-down and views data exactly as before.
3. **Resource consistency** – when a resource's hours change, the hover tooltip, calculations and project totals
   update everywhere that resource is tagged.
4. **No over-allocation** – a resource's total across all projects can never exceed its capacity (max 8 h per
   working day).

### End-date example (today Oct 2026; P1 ends Jun 2027, P2 Aug 2028, P3 Dec 2027)
| Selection | Months shown | P1 editable | P2 editable | P3 editable |
|---|---|---|---|---|
| P1 | Oct 2026 – Jun 2027 | → Jun 2027 | – | – |
| P1, P2 | Oct 2026 – Aug 2028 | → Jun 2027 | → Aug 2028 | – |
| P1, P2, P3 | Oct 2026 – Aug 2028 | → Jun 2027 | → Aug 2028 | → Dec 2027 |

Edge cases: no end date ⇒ editable throughout (12-month horizon if no selected project has one); all projects
ended ⇒ current month shown, read-only.

---

## Part B – Backend design and API

### Identity (login)
The gateway validates the Azure AD token and forwards the user's email as `x-user-email` (claims `email` →
`preferred_username` → `upn`; client-supplied values are dropped; `AUTH_ENABLED=false` uses `DEV_USER_EMAIL`).
The project service maps it to `gold.ClearOps_Users` (case-insensitive `Email`). No email → 401; unknown user →
403. The client never sends a user id.

### Table `stp_settings` = `gold.ClearOps_STPSettings`
| Column | Type | Notes |
|---|---|---|
| `STP_Setting_Id` | BIGINT identity PK | |
| `User_Id` | BIGINT FK `ClearOps_Users.User_ID` | from the login |
| `Filter_Name` | NVARCHAR(200) | unique per user |
| `Project_Ids` | JSON | list of `Project_Master.Project_Id` |
| `Selected_Projects` | JSON | `{id: {project_number, project_name, project_end_date}}` |
| `Date_Time` + Gold audit columns | | |

### Endpoints (gateway path `/api/project/stp/...`)
| Purpose | Call | Key response |
|---|---|---|
| Months + editability | `POST /stp/timeline` `{project_ids}` | `months[]`, `projects[]{project_id,end_month,rate_editable,editable_months[]}` |
| My queries | `GET /stp/settings` | list of saved queries |
| Save query (same name overwrites) | `POST /stp/settings` `{filter_name,project_ids}` | saved row |
| Apply query | `GET /stp/settings/{id}/apply` | `project_ids`, `months`, `projects` |
| Delete query | `DELETE /stp/settings/{id}` | 204 (own queries only; others → 404) |
| Save hours cell | `PUT /stp/cell` `{resource_id,task_id,year_month,hours,rate?}` | `tooltip`, `project_totals`, `projects_affected` |
| Hover refresh | `GET /stp/resources/{id}/summary?year_month=&project_id=` | same shape |

Generic CRUD for the table is also available at `/api/clearops_stpsettings`.

### Capacity and propagation
* Capacity per month = working days (Mon–Fri) × daily hours, daily hours = `min(8, WeeklyHours/5)` (8 if unknown).
  Holidays and time off are **not** deducted. Example: Nov 2026 = 21 days × 8 h = 168 h.
* All figures are derived from `ClearOps_ProjectSTP` rows joined to `ProjectWBS.Project_Id`, so every project
  sees the same data: tooltip = capacity, this-project hours, other-projects hours, remaining hours and %;
  project totals (hours, value per month and in total) are recomputed from the rows.
* `PUT /stp/cell` saves (value = hours × rate, rate falls back to the rate card), enforces the end-date window
  and capacity, and returns everything needed to refresh every affected project.
* Errors: 422 outside the editable window ("… outside the editable window …") or over capacity
  ("Over-allocation … at most N h allowed here"; nothing saved). Lowering hours is always allowed.

---

## Part C – Frontend implementation prompt

Paste everything in this part into Claude Code in the **frontend** repo.

### Role and ground rules
You are a senior front-end engineer extending the ClearOps Strategic Time Planner page.
1. Read the existing STP code first (grid, project sections, resource rows, tooltip, Save button, store) and
   reuse components, API client, styling and test setup. Add no new libraries.
2. **If an implementation of a listed feature already exists** (month range, editability, saved queries,
   tooltip/total calculations, capacity checks), **replace it** with the behaviour specified here – delete the
   old logic and its dead code/tests instead of layering a second version on top. Only add what is missing.
   Change nothing unrelated; keep all other behaviour identical.
3. The server is the source of truth for capacity, end-date windows and ownership; client checks are only for
   fast feedback. Never send a user id.
4. Work in the order below; run lint, type-check and tests after each step; finish with a summary.

### 1 · Month columns and end-date editing
- Call `POST /stp/timeline` whenever the project selection changes (debounce, cancel stale requests).
- Columns = `months`. A project's rate and monthly-hours inputs are enabled only for months in its
  `editable_months`; others are greyed/disabled but still show hours and value. Rate is disabled when
  `rate_editable` is false. Verify against the example table in Part A.

### 2 · Saved queries
- **Save Query** button beside **Save**, disabled while no project is selected.
- Modal: one text input (**Enter Query Name**, trimmed, required, max 200), **Save** and **Cancel**; Enter saves,
  Esc cancels, focus trapped and restored. Save → `POST /stp/settings`, close, refresh list, preselect, toast.
  Confirm before overwriting an existing name.
- Dropdown beside Save: my queries (alphabetical) plus an empty "No saved query" option (default).
- **A saved query is optional.** With none selected (the default), the existing functionality stays in place:
  the user can open the **project drop-down**, select one or more projects and view their data; the timeline,
  editing rules and resource checks apply to that manual selection exactly as they do for a saved query. Selecting a query → `apply` → set the project selector to its `project_ids`
  (still editable) and load the grid. Clearing the dropdown keeps current projects and data (no reset).
  Skip saved projects that no longer exist and show a notice. Optional delete icon (confirm, then `DELETE`).

### 3 · Resource consistency and no over-allocation
- One shared store keyed by `resource_id|year_month` (hours per project, capacity, other-project hours,
  remaining). Every tooltip and total reads from it, never from a row-local copy.
- On hours input: update the store optimistically, debounce, `PUT /stp/cell`. On success replace store data and
  all totals (row, month, section, header) for **every** project in `projects_affected`. On error roll back
  and show the server `detail`.
- Cap each hours input at `capacity − other_projects_hours`; above it show "Only N h left for <resource> in
  <month>" and do not send (server 422 still enforces it). Lowering is always allowed.
- Tooltip: remaining capacity (hrs and %), this project hrs, other projects hrs; negative shown red.
- A rate change recalculates value for that resource's editable months in every project it is tagged on.

### 4 · Quality bar
Accessibility (labelled inputs, reason text for locked months, keyboard-operable modal/dropdown); memoised
cells and one request per edit; tests for the editability helper (three scenarios, no end date, ended project),
cross-project propagation, the capacity cap, Save Query enabled/disabled, modal flow and apply-query filtering.

### 5 · Done when
- [ ] Columns and editability match the examples; locked cells cannot be edited.
- [ ] With no saved query selected, the user can pick projects and view data as before.
- [ ] Save Query is disabled with no selection; save, list and apply work; only my queries appear.
- [ ] Editing a resource in project A updates its tooltip and totals in project B immediately.
- [ ] A resource can never exceed capacity (client cap + server 422 handled).
- [ ] Lint, type-check and tests pass; no unrelated changes.
