# Prompt – Strategic Time Planner (STP) enhancements

Copy everything below the line into Claude Code / your frontend repo. The backend already exists (see
`docs/STP_Enhancements.md`); this prompt covers the **UI wiring** and any backend gaps.

---

You are working on the ClearOps **Strategic Time Planner (STP)** page: a grid with one section per selected
project, columns = months, rows = project → LABOR / PASS THROUGH / IC TASK → tasks → resources (rate input +
monthly hours input, value shown under each cell, a capacity tooltip on hover). First inspect the existing code
and reuse what is there; only add what is missing. Do not change behaviour that is not listed here.

## 1. Month columns and end-date editing
- Call `POST /api/project/stp/timeline` with the selected `project_ids` whenever the selection changes
  (gateway route: `/api/<service>/<path>`; the project service serves `/api/stp/...`).
- Columns = `months` from the response: **current month → latest project end month** among selected projects.
- Per project, a rate input and a monthly-forecast input are enabled only for months in that project's
  `editable_months`; all other cells are read-only (visibly disabled). The rate input is disabled when
  `rate_editable` is false.
- Examples (today Oct 2026; P1 ends Jun 2027, P2 Aug 2028, P3 Dec 2027): {P1} → Oct 2026–Jun 2027;
  {P1,P2} → Oct 2026–Aug 2028 with P1 editable to Jun 2027 and P2 to Aug 2028; {P1,P2,P3} → same columns,
  P3 editable to Dec 2027.
- A project with no end date is editable in every shown month.

## 2. Saved queries
1. Add a **Save Query** button next to **Save**; disabled until at least one project is selected.
2. Click opens a modal: one text box labelled **Enter Query Name**, buttons **Save** and **Cancel**
   (Save disabled for a blank name; Enter submits; Escape cancels).
3. Save → `POST /api/project/stp/settings` `{ filter_name, project_ids }`. Never send a user id – the owner is
   taken from the SSO login on the server (401 not signed in, 403 no ClearOps user). Same name overwrites.
4. Show a dropdown next to Save listing `GET /api/project/stp/settings` (`filter_name`), refreshed after saving.
5. Choosing a query → `GET /api/project/stp/settings/{id}/apply` and set the project filter to the returned
   `project_ids` (then reload the timeline). Clearing/not choosing a query leaves existing behaviour untouched.
6. Optional: a delete icon per query → `DELETE /api/project/stp/settings/{id}`.
Handle errors with a toast; do not lose the user's current selection on failure.

## 3. Resource consistency (tooltip + calculations)
- When a resource's hours cell is edited, save with `PUT /api/project/stp/cell`
  `{ resource_id, task_id, year_month, hours, rate? }` (value = hours × rate).
- Use the single response to refresh **every** place that resource appears: `projects_affected` lists all
  projects; replace each section's hours/value cells, row/month/project totals and header totals from
  `project_totals`, and update the capacity tooltip (this project / other projects / remaining hrs and %,
  red when `over_allocated`) from `tooltip`. No stale values anywhere after a save.
- Tooltips on hover must read from the same shared client store keyed by `resource_id + year_month`, not from
  per-row copies. Optimistically update the store on input, reconcile with the response, roll back on error.
- **Never over-allocate:** limit each hours input to `capacity − other_projects_hours` for that resource/month, show an inline message when exceeded, and surface the server's 422 ("Over-allocation …") by reverting the cell. Lowering hours is always allowed.
- Rate edits must also recalculate value (hours × rate) for the resource's editable months in all projects.

## 4. Acceptance checklist
- [ ] Column range and per-project editability match the examples above.
- [ ] Save Query disabled with no projects; modal flow works; dropdown lists only my queries.
- [ ] Selecting a query filters the grid to its projects; otherwise nothing changes.
- [ ] Editing a resource in project A updates its tooltip and totals in project B in the same view.
- [ ] A resource cannot exceed monthly capacity across projects (client cap + server 422).
- [ ] Server 422 (outside end date) is surfaced and the cell reverts.
- [ ] Unit tests for the editability helper and the shared store; existing tests still pass.

Finish with a short summary of files changed and anything you could not verify.
