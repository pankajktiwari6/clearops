# Forecast grid: persist edits on Save and refresh the capacity tooltip

## Requirement
1. Editing the hours input for one or more resources, then clicking **Save All Forecasts**, must write those values to the database for each resource, and the change must show everywhere the data is used.
2. The hover tooltip ("Capacity available": *Remaining / This project / Other projects*) must be recomputed for the resource across **all projects allocated to that resource**, not only the open project.

## Findings from the repo
- This repo has **no frontend code** (no JS/TSX/Vue). The forecast grid and tooltip (MUI) live in a separate UI codebase, so the UI changes below are not implemented here.
- The backend is a generic, mapping-driven CRUD layer: `ClearOps_App/app/api/crud.py` builds one router per entry in `ClearOps_App/app/column_mapping.json` (list, get, POST, PATCH, DELETE). The microservices in `clearops_microservices/services/*` only select which tables each service owns.
- Forecast hours map to `gold.ClearOps_ProjectTimePlanner` (`ClearOps_App/app/models/project_time_planner.py`), served by `timeplanner-service`. Relevant columns: `Resource_Id`, `Task_ID` (to `ProjectWBS`, hence project), `StartDate`/`EndDate`, `PlanHours`, `IsActive`.
- Capacity inputs: `gold.Resources.WeeklyHours` (`ClearOps_App/app/models/resource.py`).
- Nothing in the backend currently does bulk save or cross-project capacity aggregation.

## Proposed changes
### Backend
1. **Bulk save endpoint** (timeplanner service), e.g. `PUT /projecttimeplanner/bulk`:
   - Body: list of `{resource_id, task_id, month/start_date/end_date, plan_hours}`.
   - Upsert per (`Resource_Id`, `Task_ID`, period) in **one transaction** (all or nothing); stamp audit columns from `x-user`.
   - Return the saved rows plus recomputed capacity per affected resource.
2. **Capacity endpoint**, e.g. `GET /capacity?resource_ids=..&from=..&to=..`:
   - Per resource and month: `capacity = WeeklyHours x working days/5` (minus holidays/time off if applicable).
   - `this_project` = sum of `PlanHours` for the current project's tasks.
   - `other_projects` = sum of `PlanHours` for the same resource on **all other** projects (active rows only).
   - `remaining = capacity - this_project - other_projects`; percent = remaining / capacity.
   - Single grouped SQL query (join `ProjectTimePlanner` to `ProjectWBS` for project); no per-cell calls.

### Frontend (separate repo)
1. Track dirty cells by (resource, month); enable **Save All Forecasts** / **Clear All** only when dirty.
2. On Save, send one bulk request with all dirty cells; on success clear dirty state and refetch/invalidate grid rows, row/column totals, revenue cards and the capacity query. On failure, keep edits and show an error.
3. Tooltip reads from the capacity endpoint (keyed by resource + month) instead of local values, so it reflects other projects. Refetch after save.
4. Optionally recompute the tooltip optimistically while typing: `remaining = capacity - other_projects - edited_this_project`.

## Acceptance criteria
- Editing 120 -> 130 for a resource and saving persists `PlanHours` in the DB; a page reload shows 130.
- Editing several resources/months and saving updates all of them atomically.
- Totals, revenue and other views using the same data show the new values after save.
- Tooltip "Other projects" equals the resource's hours on all other active projects; "Remaining" = capacity - this project - other projects.
- Failed save leaves the DB unchanged and keeps edits in the UI.

## Open questions
- Where is the UI repo, and which table is the grid's source of truth (`ProjectTimePlanner` vs `ProjectEstimator`)? Hours are stored per task/date range; monthly cells need a defined mapping.
- Capacity definition: use `WeeklyHours` only, or also holidays and time off (`Holiday`, `TimeOff`, `WorkdayEmployeeTimeOff`)?
