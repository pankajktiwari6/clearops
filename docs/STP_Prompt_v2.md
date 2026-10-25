# STP Enhancements – Implementation Prompt (v2)

Paste everything below the line into Claude Code in the **frontend** repo. Backend contract is final
(see `docs/STP_Enhancements.md`); it is served through the gateway as `/api/project/stp/...`.

---

## Role and ground rules
You are a senior front-end engineer extending the ClearOps **Strategic Time Planner (STP)** page.
1. Read the existing STP code first (grid, project sections, resource rows, tooltip, Save button, state/store).
   Reuse existing components, hooks, API client, styling and test setup. Do not add new libraries.
2. Change only what this prompt lists; keep all other behaviour identical.
3. The server is the source of truth: never compute capacity, end-date windows or ownership on the client
   beyond what the responses give you. Client checks are only for fast feedback.
4. Work in small steps (section order below), run lint, type-check and tests after each, then summarise.

## Backend contract (all JSON, auth via the existing SSO bearer token; never send a user id)
| Purpose | Call | Key response fields |
|---|---|---|
| Months + editability | `POST /stp/timeline` `{project_ids}` | `months[]` ("YYYY-MM"), `projects[]{project_id,end_month,rate_editable,editable_months[]}` |
| List my queries | `GET /stp/settings` | `[{stp_setting_id,filter_name,project_ids}]` |
| Save query (same name overwrites) | `POST /stp/settings` `{filter_name,project_ids}` | saved row |
| Apply query | `GET /stp/settings/{id}/apply` | `project_ids`, `months`, `projects` |
| Delete query | `DELETE /stp/settings/{id}` | 204 |
| Save hours cell | `PUT /stp/cell` `{resource_id,task_id,year_month,hours,rate?}` | `tooltip`, `project_totals`, `projects_affected` |
| Hover refresh | `GET /stp/resources/{id}/summary?year_month=&project_id=` | same as above |
Errors: 401 not signed in · 403 no ClearOps user · 404 unknown/not yours · 422 outside end-date window **or
over-allocation** (show `detail` in a toast/inline message and revert the cell).

## 1 · Month columns and end-date editing
- Fetch the timeline whenever the project selection changes (debounce, cancel stale requests).
- Columns = `months` (current month → **max** end month of all selected projects).
- A project's rate input and monthly-hours inputs are enabled **only** for months in that project's
  `editable_months`; others render disabled/greyed. Rate input is disabled when `rate_editable` is false.
- Example (today Oct 2026; P1 ends Jun 2027, P2 Aug 2028, P3 Dec 2027): {P1} → Oct 26–Jun 27;
  {P1,P2} → Oct 26–Aug 28, P1 editable to Jun 27, P2 to Aug 28; {P1,P2,P3} → same columns, P3 editable to Dec 27.
- No end date ⇒ editable in all shown months. Disabled cells still display hours and value.

## 2 · Saved queries
- **Save Query** button beside **Save**, disabled while no project is selected.
- Click → modal: one text input (label/placeholder **Enter Query Name**, trimmed, max 200 chars, required),
  **Save** and **Cancel**. Enter = save, Esc = cancel, focus trapped, focus returns to the button on close.
- Save → `POST /stp/settings`; on success close the modal, refresh the list, preselect the new query, toast.
  Reusing a name overwrites – confirm with the user first if the name already exists in the list.
- Dropdown beside Save lists my queries (alphabetical) with an empty "No saved query" option.
  Selecting a query → `apply` → set the project filter to `project_ids` and reload the grid.
  Selecting "No saved query" or changing the selection manually leaves current behaviour untouched.
- Optional delete icon per option (confirm, then `DELETE`).

## 3 · Resource consistency and no over-allocation
- Keep one shared client store keyed by `resource_id|year_month` holding hours per project, capacity,
  other-project hours, remaining hours/%. Every tooltip and total reads from it, never from a row-local copy.
- On hours input: update the store optimistically; debounce, then `PUT /stp/cell`. On success, replace store data
  and every total for **each** project in `projects_affected` (row, month, section and header totals; value =
  hours × rate). On error, roll back to the last saved value and show the message.
- Cap each hours input at `capacity − other_projects_hours` (from the store). Above the cap: inline error
  "Only N h left for <resource> in <month>", do not send. The server still enforces this (422).
  Lowering hours is always allowed. Resources without capacity data have no cap.
- Tooltip content: capacity remaining (hrs and %), this project hrs, other projects hrs. Remaining < 0 shown red.
- A rate change recalculates value for that resource's editable months in every project it is tagged on.

## 4 · Quality bar
- Accessibility: labelled inputs, `aria-disabled`/reason text for locked months, keyboard-operable modal/dropdown.
- Performance: memoise cells; one request per edit; never re-render the whole grid for one cell.
- Tests: editability helper (the three scenarios plus no-end-date and ended project), shared-store propagation
  across two projects, over-allocation cap, Save Query disabled/enabled, modal flow, apply-query filtering.

## 5 · Done when
- [ ] Columns and editability match the examples; locked cells cannot be edited.
- [ ] Save Query is disabled with no selection; modal, save, list and apply work; only my queries appear.
- [ ] Editing a resource in project A updates its tooltip and totals in project B immediately.
- [ ] A resource can never exceed monthly capacity across projects (client cap + server 422 handled).
- [ ] Lint, type-check and tests pass; no unrelated changes.

Final reply: files changed, how you tested, and anything you could not verify.
