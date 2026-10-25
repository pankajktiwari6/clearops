# Strategic Time Planner: resource-level sync

## Problem
In the Strategic Time Planner grid the same resource (e.g. Nitu Khatri) can be staffed on several
projects/tasks. Editing a resource field must update every place that resource is tagged, and the
change must be saved to the database, not only held in the UI.

## Where data is stored
| Grid field | Table | Column |
|---|---|---|
| Monthly hours (cell) | `gold.ClearOps_ProjectSTP` | `Monthly_Hours` (keyed by `Resorce_id`, `task_id`, `Year_Months`) |
| Cell value (CA$) | `gold.ClearOps_ProjectSTP` | `Monthly_Value` = hours x rate |
| Rate (per resource) | `gold.ClearOps_RateCard` | `Rate` (one card per resource, `Desciption = 'Resource:<id>'`) |
| Rate link | `gold.ClearOps_ProjectSTP` | `Rate_Card_Id` on every row of the resource |

## Endpoints (project service, via gateway `/api/project/...`)
- `PUT /api/clearops_projectstp/resource/{resource_id}/rate` body `{"rate": 120}`
  Upserts the resource's rate card, points **all** of the resource's STP rows (every project/task) at it,
  and recomputes each `Monthly_Value`. Returns every updated row.
- `PUT /api/clearops_projectstp/resource/{resource_id}/hours` body `{"task_id": 1, "year_months": "Oct 2026", "monthly_hours": 16}`
  Upserts that cell, sets `Monthly_Value` from the resource's rate, and returns `monthly_totals`
  (hours per month across all projects) so other views of the resource (capacity tooltip,
  other project rows) can refresh.

Both stamp `GoldModifiedBy/GoldModifiedDate` from the `X-User` header.

## Frontend wiring
After a successful call, replace the local state for the returned `rows` and `monthly_totals`
for that resource in every project block where it appears (match on `resorce_id`).

## Assumption to confirm
Rate edits propagate to all projects. Hours edits are saved per project/task cell (hours differ by
project), but the resource's cross-project totals are refreshed everywhere. If hours should also be
copied to every project, say so and the hours endpoint can fan out.

Code: `ClearOps_App/app/api/resource_sync.py`, registered in `ClearOps_App/app/main.py`.
