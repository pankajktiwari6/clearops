# STP Forecast Page: Project End Dates and Saved Queries

| | |
|---|---|
| **Page** | STP (Forecast) |
| **Scope** | Two features: (A) end-date-driven month range and edit permissions, (B) saved project queries |
| **Layers** | React frontend (separate repo) and this repo's FastAPI backend (gold schema, project service, gateway) |

---

## 1. Background: current vs. target UI

| State | Today | Target |
|---|---|---|
| No project selected | `Projects` multi-select; Transfer, Bulk Allocation, Export, Clear All and Save All Forecasts are disabled; KPI tiles show 0; banner says "Select one or more projects to load their forecast." | Unchanged, plus **Save Query** (disabled) and **Saved Query** dropdown next to the Projects dropdown |
| Projects selected | Grid shows a **fixed 6 months** (Oct 2026 to Mar 2027) plus Total. Rows are nested: Project, LABOR, 01.Fee, then resources. Each resource has an editable Rate and an editable hours input per month. | Month range and editable cells are driven by project end dates (Feature A). **Save Query** is enabled. |

---

## 2. Feature A: End-date-driven months and edit permissions

**Source field:** `gold.Project_Master.Project_End_Date` (API `project_end_date`).

### 2.1 Rules
1. **Displayed months** run from the **current month** to the **latest end-date month** among the selected projects. This replaces the fixed 6-month window. Recalculate on every selection change.
2. **Editable cells:** a project's **Rate** and **monthly forecast (hours)** inputs are editable only from the current month through **that project's own end-date month**, inclusive.
3. Cells after a project's end month, but within the displayed range, are **read-only**. They get a tooltip such as "Project ended Jun 2027".
4. Dates are compared at **year-and-month** granularity.
5. Past months and the no-selection state keep today's behavior.
6. **Null end date** is treated as unrestricted: editable through the end of the displayed range. *(Assumption, to be confirmed. See section 7.)*

### 2.2 Scenarios (today = Oct 2026; P1 ends Jun 2027, P2 ends Aug 2028, P3 ends Dec 2027)

| # | Selected | Months shown | P1 editable | P2 editable | P3 editable |
|---|---|---|---|---|---|
| 1 | P1 | Oct 2026 – Jun 2027 | Oct 2026 – Jun 2027 | n/a | n/a |
| 2 | P1, P2 | Oct 2026 – Aug 2028 | Oct 2026 – Jun 2027 | Oct 2026 – Aug 2028 | n/a |
| 3 | P1, P2, P3 | Oct 2026 – Aug 2028 | Oct 2026 – Jun 2027 | Oct 2026 – Aug 2028 | Oct 2026 – Dec 2027 |

### 2.3 Implementation
- Two pure, shared helpers. Components must not contain date math.
  - `getDisplayMonthRange(selectedProjects, today) -> Month[]`
  - `isMonthEditable(project, month, today) -> boolean`
- The same editable check applies to **every write path**, not only the inputs:
  - **Bulk Allocation** and **Transfer** skip or reject read-only months.
  - **Save All Forecasts** sends only cells in each project's editable range.
- Totals, KPI tiles and Export must work for the dynamic range.
- Defense in depth (recommended): the forecast save API also rejects writes after a project's end month.

### 2.4 Tests
- The three scenarios above.
- A null end date.
- An end date before the current month.
- Deselecting the project with the latest end date shrinks the range.
- Bulk Allocation and Transfer do not touch read-only months.

---

## 3. Feature B: Save Query and Saved Query dropdown

### 3.1 User flow
1. **Save Query** button: right of the Projects dropdown, **disabled until at least one project is selected**.
2. Click opens a modal with one text box (**"Enter Query Name"**) and **Save** / **Cancel** buttons.
3. Validation:
   - the name is required, trimmed, and at most 100 characters
   - a duplicate name for the same user shows an inline error
   - Save is disabled while the request is in flight
4. On Save, the modal closes, a success toast appears, and the name appears in the **Saved Query** dropdown immediately, **with no page reload**.
5. **Selecting a saved query** replaces the current project selection and the grid loads automatically, **with no page reload**. Feature A recalculates the range and permissions.
   - Saved projects that no longer exist are skipped, with a notice such as "2 projects no longer available".
6. **Otherwise, existing behavior is unchanged.** Manually selecting projects works exactly as today. Selecting a saved query never blocks later manual changes.
7. The dropdown is populated when the STP page opens, so it is ready right after login.
8. Recommended: a per-query delete action with a confirm step.

### 3.2 Frontend implementation
- Use the app's existing data-fetching approach. If none exists, use **TanStack Query**.
  - `useQuery(['stp-settings'])` loads the list.
  - `useMutation` saves and deletes, then calls `invalidateQueries`. This is what keeps the UI fresh without a reload.
- Wrap it all in one hook, `useStpSavedQueries()`.
- Reuse the existing modal, select and toast components.
- Optional: mirror the selection in the URL (`?projects=12,45,78`) so a browser refresh keeps it. The URL takes priority on load.

---

## 4. Data model: `gold.ClearOps_STP_Settings`

ClearOps-owned table. It follows the repo conventions: `GoldAuditColumnsMixin`, model in `app/models/`, schema in `app/schemas/`, entry in `column_mapping.json`, owned by the **project** domain service.

| Column | Type | Notes |
|---|---|---|
| `STP_Setting_Id` | BIGINT, PK, identity | |
| `User_ID` | BIGINT, FK → `gold.ClearOps_Users.User_ID` | Resolved from the login, never taken from the request body |
| `Filter_Name` | NVARCHAR(100) | `UNIQUE (User_ID, Filter_Name)` |
| `Selected_Projects` | NVARCHAR(MAX), JSON | `{"project_ids": [12, 45, 78]}`, a list of `gold.Project_Master.Project_Id` |
| `Date_Time` | DATETIME2 | Default UTC now |
| Audit columns | via `GoldAuditColumnsMixin` | |

- Index on `User_ID`.
- **JSON IDs cannot carry foreign keys**, so the API validates every ID against `Project_Master` before saving.
- Store IDs only, not names or dates. End dates are always read live, so saved queries never go stale.

---

## 5. API

Endpoints are scoped to the authenticated user.

| Method | Path | Behavior |
|---|---|---|
| GET | `/api/project/clearops_stp_settings` | List the current user's queries (id, name, project IDs), sorted by name |
| POST | `/api/project/clearops_stp_settings` | Body `{ "filter_name", "project_ids" }`. 201 on success. 400 for a blank name, an empty list or unknown IDs. 409 for a duplicate name. |
| DELETE | `/api/project/clearops_stp_settings/{id}` | 204 on success. 404 for another user's row. |

### 5.1 Identity and security
- The gateway validates the Azure AD token. It currently forwards **no identity** to the services, so it must forward the user claim (email or `oid`) as a header.
  - Services must **only trust that header from the gateway**, not from external callers.
- The service resolves the claim to `ClearOps_Users.User_ID`. If it is not found, return 403.
- The generic mapping-driven CRUD is **not user-scoped**. Do not expose this table through it. Use a custom router that filters on the resolved `User_ID`.
- Gateway GET responses are cached in Redis. Make sure the cache key varies by user, or skip caching for this path, so users never see each other's queries.

---

## 6. Delivery plan and acceptance

### 6.1 Order of work
1. Feature A helpers and tests, then wire into the grid, Bulk Allocation, Transfer and Save.
2. Migration, model, schema, custom router, gateway identity forwarding, and API tests.
3. Frontend hook, modal and dropdown.
4. Run lint, typecheck and tests.

### 6.2 Acceptance checklist
- [ ] The month range ends at the latest end month among the selected projects.
- [ ] Rate and hours are editable only through each project's own end month, in all write paths.
- [ ] Scenarios 1 to 3 pass in unit tests.
- [ ] Save Query is disabled with no selection.
- [ ] The modal has "Enter Query Name", Save and Cancel, with validation and duplicate handling.
- [ ] A saved query appears in the dropdown with no page reload.
- [ ] Selecting a saved query loads its projects and refreshes the grid with no reload.
- [ ] Manual project selection behaves as before.
- [ ] `ClearOps_STP_Settings` exists, scoped to the logged-in user.
- [ ] API tests cover user scoping, duplicates, invalid IDs and a missing user.
- [ ] Gateway caching cannot leak queries across users.

---

## 7. Open questions
1. **Null end date:** unrestricted (current assumption) or fully read-only?
2. Should the last-applied query be remembered across sessions?
3. Should queries be shareable between users? The current scope is per user only.
4. Which repository holds the React frontend? It isn't in this repo, so only the backend can be built here.
