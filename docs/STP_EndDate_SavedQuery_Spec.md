# STP Page: Project End-Date Rules and Saved Queries

Requirements and implementation spec for the Forecast (STP) page.

## 1. Current UI (from the screenshots)

| Screenshot | State | Observations |
|---|---|---|
| 1 | No project selected | `Projects` multi-select dropdown. Toolbar buttons (`Transfer`, `Bulk Allocation`, `Export`, `Clear All`, `Save All Forecasts`) are disabled. KPI tiles show `Total Staffed Hours` and `Raw/List Revenue` as 0. An info banner reads "Select one or more projects to load their forecast." |
| 2 | Projects selected (one chip shown, `+2` more) | The grid loads for each project. Columns are `Name`, `Rate`, then months (Oct 2026 to Mar 2027, plus a `Total` column). The month range is currently fixed to 6 months. Rows are nested: Project, LABOR, 01.Fee, then resource rows. Each resource row has an editable Rate input and an editable hours input per month. `Transfer`, `Bulk Allocation` and `Export` are enabled. |
| 3 | Target design (mock-up) | Next to the Projects dropdown there are a **Save Query** button (orange) and a **Saved Query** dropdown. |

## 2. Feature A: End-date-driven months and edit permissions

### Rules
1. **Displayed months**: from the **current month** to the **latest `project_end_date` month** among all selected projects. This replaces the fixed 6-month window. The range recalculates on every selection change.
2. **Editable cells**: for each project, the **Rate** input and the **monthly forecast (hours)** inputs are editable only from the current month through that project's **own** end-date month, inclusive.
3. Months after a project's end date, but still displayed because another selected project ends later, are **read-only/disabled**. Show a tooltip such as "Project ended Jun 2027".
4. Comparison is at month granularity (year and month), not by day.
5. Past months keep today's behavior.
6. If no project is selected, keep the existing default behavior.
7. If a project's end date is null, treat it as not restricted by end date (editable through the end of the displayed range). **Assumption, to be confirmed.**

Source field: `Project_Master.Project_End_Date` (API: `project_end_date`).

### Scenarios (today = Oct 2026)

Project end dates: P1 = Jun 2027, P2 = Aug 2028, P3 = Dec 2027.

| # | Selected | Months shown | P1 editable | P2 editable | P3 editable |
|---|---|---|---|---|---|
| 1 | P1 | Oct 2026 – Jun 2027 | Oct 2026 – Jun 2027 | n/a | n/a |
| 2 | P1, P2 | Oct 2026 – Aug 2028 | Oct 2026 – Jun 2027 | Oct 2026 – Aug 2028 | n/a |
| 3 | P1, P2, P3 | Oct 2026 – Aug 2028 | Oct 2026 – Jun 2027 | Oct 2026 – Aug 2028 | Oct 2026 – Dec 2027 |

### Implementation notes
- Put two pure helpers in a shared util. Components must not contain date math.
  - `getDisplayMonthRange(selectedProjects, today)` returns the list of months.
  - `isMonthEditable(project, month, today)` returns a boolean.
- Totals, KPI tiles and `Save All Forecasts` must keep working with the dynamic range. Save only cells in each project's editable range.
- `Bulk Allocation` and `Transfer` must also respect the per-project editable range.
- Unit tests:
  - the three scenarios above
  - a null end date
  - an end date before the current month
  - deselecting the project that has the latest end date

## 3. Feature B: Save Query and Saved Query dropdown

### UX flow
1. **Save Query** button sits right of the Projects dropdown.
   - It is **disabled** until at least one project is selected.
2. Clicking it opens a modal:
   - one text box, label/placeholder **"Enter Query Name"**
   - **Save** and **Cancel** buttons
3. The user types a name and clicks **Save**.
   - Validation: required, trimmed, max 100 characters.
   - A duplicate name for the same user shows an inline error.
   - Save is disabled while the request is in flight.
4. After Save, the modal closes, a success toast appears, and the new name appears in the **Saved Query** dropdown, next to the button, **without a page reload**.
5. **Selecting a saved query** replaces the current project selection with the saved projects.
   - The grid loads automatically, with no page reload.
   - Feature A recalculates the month range and edit permissions.
   - If any saved project no longer exists, skip it and show a small notice such as "2 projects no longer available".
6. **Otherwise**, with no saved query chosen, the existing functionality is unchanged. Manually picking projects works exactly as today.
7. The dropdown is loaded when the STP page opens, so it is populated right after login.
8. Optional but recommended: a delete action per saved query, with a confirm step.

### Frontend implementation notes
- Use the app's existing data-fetching approach. If there is none, use TanStack Query.
  - `useQuery(['stp-settings'])` loads the list.
  - `useMutation` saves and deletes, then calls `invalidateQueries` so the dropdown refreshes with no reload.
- Wrap this in one hook, `useStpSavedQueries()`.
- Reuse the existing modal, select and toast components.
- Optionally mirror the active selection in the URL (`?projects=…`) so a browser refresh keeps it. If present, the URL selection takes priority on load.

## 4. Data model: `ClearOps_STP_Settings`

New ClearOps-owned table in the `gold` schema, following the repo's conventions (`GoldAuditColumnsMixin`; see `ClearOps_App/app/models/project_stp.py`).

| Column | Type | Notes |
|---|---|---|
| `STP_Setting_Id` | BIGINT, PK, identity | |
| `User_ID` | BIGINT, FK → `gold.ClearOps_Users.User_ID` | Resolved from the logged-in user, never from the request body |
| `Filter_Name` | NVARCHAR(100) | `UNIQUE (User_ID, Filter_Name)` |
| `Selected_Projects` | NVARCHAR(MAX), JSON | `{"project_ids": [12, 45, 78]}`, a list of `gold.Project_Master.Project_Id` |
| `Date_Time` | DATETIME2, default UTC now | |
| audit columns | from `GoldAuditColumnsMixin` | |

- Add an index on `User_ID`.
- A JSON column cannot carry foreign keys, so the API must validate that every ID exists in `Project_Master` before saving.
- Add the table to `column_mapping.json`, with a model in `app/models/` and a schema in `app/schemas/`. Assign it to the **project** domain service (`clearops_microservices/services/project/service.py`).

## 5. API

Scoped to the authenticated user. The gateway validates the Azure AD token and must forward the user's identity (for example email or `oid` claim) to the domain service. The service resolves it to `User_ID`.

| Method | Path | Behavior |
|---|---|---|
| GET | `/api/project/clearops_stp_settings` | List the current user's saved queries |
| POST | `/api/project/clearops_stp_settings` | Body `{ "filter_name": "...", "project_ids": [..] }`. 201 on success; 400 for a blank name, an empty list or unknown project IDs; 409 for a duplicate name |
| DELETE | `/api/project/clearops_stp_settings/{id}` | Delete; 404 for another user's row |

Do not use the generic mapping-driven CRUD for this table as-is: it is not user-scoped. Use a custom router that filters on the logged-in `User_ID`.

## 6. Acceptance checklist
- [ ] The month range ends at the latest end date among the selected projects.
- [ ] Rate and hours cells are editable only through each project's own end month.
- [ ] Scenarios 1 to 3 pass in unit tests.
- [ ] Save Query is disabled with no selection.
- [ ] The modal has "Enter Query Name", Save and Cancel; validation and duplicate handling work.
- [ ] The saved query appears in the dropdown without a page reload.
- [ ] Selecting a saved query applies its projects and refreshes the grid without a reload.
- [ ] Existing manual project selection is unchanged.
- [ ] `ClearOps_STP_Settings` is created, with the user scoped from the login.
- [ ] API tests cover user scoping, duplicates and invalid project IDs.

## 7. Open questions
1. What should happen when a project's end date is null? The current assumption is unrestricted.
2. Should the last-applied query be remembered across sessions?
3. Should queries be shareable between users? The current scope is per user only.
4. The frontend code is not in this repo. Which repository holds the React app?
