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
**Principle: the backend owns every calculation.** The UI sends raw edits and renders whatever the API returns. It never sums, multiplies or derives capacity itself.

### Backend
1. **Bulk save endpoint** (timeplanner service), e.g. `PUT /forecast/bulk`:
   - Body: list of `{resource_id, task_id, period (month), plan_hours}` plus `project_id`. Only raw inputs, no totals.
   - Validate (hours >= 0, resource is allocated to the project, period valid), then upsert per (`Resource_Id`, `Task_ID`, period) in **one transaction** (all or nothing). Stamp audit columns from `x-user`.
   - After commit, recompute and return the full forecast view for the affected project and resources (see response below), so one round trip refreshes the screen.
2. **Forecast read endpoint**, e.g. `GET /forecast?project_id=..`: returns the same shape as the save response, used for initial load and refresh.
3. **Calculations done server-side (single grouped SQL query, no per-cell calls):**
   - Per resource-month: `cost = hours x rate`.
   - Per task/row and per column: hour and revenue totals; grand totals for the "Total Staffed Hours" and "Raw/List Revenue" cards.
   - Capacity per resource-month: `WeeklyHours x working days / 5`, minus holidays and time off if in scope.
   - `this_project` = sum of `PlanHours` for the open project's tasks.
   - `other_projects` = sum of `PlanHours` for the same resource on **all other** active projects (join `ProjectTimePlanner` to `ProjectWBS` for the project).
   - `remaining = capacity - this_project - other_projects`; `remaining_pct = remaining / capacity`; and a status (e.g. available / near / over capacity) that drives the green dot.
4. **Response shape (example):**
   ```json
   {
     "rows": [{"resource_id": 1, "months": [{"period": "2026-10", "hours": 120, "cost": 12000.0,
        "capacity": {"remaining": 53.33, "remaining_pct": 30.8, "this_project": 120,
                     "other_projects": 0, "status": "available"}}],
        "total_hours": 361, "total_cost": 36100.0}],
     "column_totals": [{"period": "2026-10", "hours": 120, "cost": 12000.0}],
     "summary": {"total_staffed_hours": 797, "raw_list_revenue": 104260.0}
   }
   ```
5. Also expose `GET /capacity?resource_ids=..&from=..&to=..` for other screens that need the same numbers, reusing the same service function so results never diverge.
6. Add unit tests for the capacity and totals calculations (multi-project resource, zero capacity, over-allocation, rounding) and an integration test for bulk save then read-back.

### Frontend (separate repo)
1. Track dirty cells by (resource, period); enable **Save All Forecasts** / **Clear All** only when dirty.
2. On Save, send one bulk request with raw edits only; on success replace grid state with the response (values, totals, cards, tooltip data). On failure keep edits and show an error.
3. Tooltip renders `capacity` from the API response as-is. No local arithmetic.
4. Optional: while typing, either show no live tooltip change until save, or call a lightweight backend "preview" endpoint (debounced) so the number still comes from the server.

## Acceptance criteria
- Editing 120 -> 130 for a resource and saving persists `PlanHours` in the DB; a page reload shows 130.
- Editing several resources/months and saving updates all of them atomically.
- Totals, revenue and other views using the same data show the new values after save.
- All totals, revenue and capacity values in the UI come from the API response; the UI does no calculation.
- Tooltip "Other projects" equals the resource's hours on all other active projects; "Remaining" = capacity - this project - other projects.
- Failed save leaves the DB unchanged and keeps edits in the UI.

## Open questions
- Where is the UI repo, and which table is the grid's source of truth (`ProjectTimePlanner` vs `ProjectEstimator`)? Hours are stored per task/date range; monthly cells need a defined mapping.
- Capacity definition: use `WeeklyHours` only, or also holidays and time off (`Holiday`, `TimeOff`, `WorkdayEmployeeTimeOff`)?
