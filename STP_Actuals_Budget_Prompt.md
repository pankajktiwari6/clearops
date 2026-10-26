# Prompt: Add Actuals and Budget to the STP screen

## Role and context
You are working in the `clearops` repo (FastAPI + SQLAlchemy backend in `ClearOps_App/`, microservices in `clearops_microservices/`). Implement the following change to the **STP (Project STP) screen**. The change comes from the call with Ajeet and team on 26 Oct 2026.

Before coding, find how the STP screen gets its data. Start with `ClearOps_App/app/models/project_stp.py`, `schemas/project_stp.py`, `api/crud.py`, `column_mapping.json` (key `ProjectSTP`) and `clearops_microservices/services/project/service.py`. Then follow the existing pattern. This repo has no UI code, so if the frontend lives elsewhere, expose the data through the API and tell me which fields the UI must render.

## Requirements
1. **Actuals next to Rate.** For every task on the STP screen, show an **Actuals** value in the column next to **Rate**.
2. **Actuals source.** Actuals come from the **Project Timecard** table (`gold.Project_Timecard`, model `ProjectTimecard`). They cover **all resources mapped to that task**. In other words, sum the timecard rows for every resource on that task, not just one resource.
3. **Budget next to Actuals.** For every task under a project on the STP screen, show a **Budget** value in the column right after Actuals.
4. **Budget source.** Budget for a task comes from the **WBS table** (`gold.ProjectWBS`), column **Current Budget Revenue** (`CurrentBudget_Revenue_ByTask`, ORM attribute `CurrentBudgetRevenueByTask`).

Resulting column order: `... | Rate | Actuals | Budget | ...`

## Data mapping
| Item | Source | Join / key |
|---|---|---|
| Task on STP row | `ProjectSTP.TaskId` | FK to `ProjectWBS.ProjectWBSId` (`Project_WBS_Id`). Do not confuse it with `ProjectWBS.TaskId`, which is a string. |
| Budget | `ProjectWBS.CurrentBudgetRevenueByTask` | Same WBS row as the STP task. |
| Actuals | `ProjectTimecard.HOURS` (aggregate) | Match on project number + task number: `ProjectTimecard.PROJECTNUM` = project's number, and `ProjectTimecard.TASKNUMBER` = `ProjectWBS.TaskNumber`. |
| Resources of a task | STP rows sharing the same task | Resource-to-timecard link is `ProjectTimecard.EMPLOYEENUMBER`. Per the call, the match is on **user + project + task**. |

Notes for the join:
- Verify the exact project-number column on `Project_Master` and the employee-number column on `Employee`/`Resources` before writing the join.
- Aggregate in SQL (`GROUP BY` task), not in Python loops. Avoid N+1 queries.
- Return `0` for Actuals when there are no timecard rows. Return `null` for Budget when the WBS value is null. Do not default Budget to `0`.

## Open question to resolve before implementing (ask me if the code does not settle it)
`Project_Timecard` stores only **hours** (`HOURS`). It has no dollar or cost column. Budget is a **revenue (currency)** value, so Actuals and Budget will be in different units unless one of these is chosen:
- **(a)** Actuals = sum of hours, shown as hours. Budget stays in currency.
- **(b)** Actuals = sum of hours × the resource's rate (the `Rate` on the STP row's rate card), shown in currency so it compares with Budget.

On the call, Actuals sits "next to Rate", which suggests (b). Default to **(b)** unless I say otherwise. Keep the calculation in one helper so switching is easy. Label units clearly in the response and the UI header.

## Constraints
- **Read-only.** Actuals and Budget are calculated for display only. Do not store them in `ClearOps_ProjectSTP`. Do not add them to `ProjectSTPCreate` or `ProjectSTPUpdate`. Add them to the response or read model only (for example `actuals` and `budget` on a new STP-screen response schema or an extended `ProjectSTPResponse`), and make them non-editable.
- Do not change existing columns or break existing API consumers. New fields are additive.
- Keep the project's existing conventions: the `column_mapping.json` entries, the `validation_alias` pattern in schemas, and the sortable-fields `Literal` if you expose these for sorting.
- Do not modify the ingestion pipeline (`data_pipeline/`) or the gold table definitions.
- Branch: develop on `claude/fervent-rubin-i7gbmb`. Do not open a PR unless I ask.

## Acceptance criteria
- Each STP task row returns `actuals` and `budget`, and they appear in that order after Rate.
- Actuals equals the sum over all resources mapped to the task, filtered to the same project and task. Test with a task that has 2 or more resources.
- Budget equals `CurrentBudget_Revenue_ByTask` of the task's WBS row.
- Tasks with no timecards show Actuals 0, and tasks with no budget show Budget null (blank in the UI).
- Add or extend tests in `clearops_microservices/tests/test_services.py` (or the app's test location) covering: multi-resource sum, no-timecard task, null budget, and cross-project isolation (same task number in another project is not counted).
- Existing tests still pass. Run lint and the test suite and report the results.

## Out of scope for this prompt (also discussed on the call, handle separately)
The call also covered these items. They are **not** part of this change:
- Budget % / productivity color coding (green / yellow / red thresholds at 100% of allocation and availability) and the "over 100%" checkbox toggle. The call did not settle the exact rules.
- Month-wise columns, and showing a single row per resource with the task columns.
- Release and branching strategy for the microservices code (code freeze, prod around Nov, hotfix branch).

## Deliverable
Summarize the files changed, the SQL or ORM query used for the aggregation, which unit option (a) or (b) you applied, and anything you could not verify.
