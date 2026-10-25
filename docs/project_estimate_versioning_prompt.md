# Implementation Prompt: Project Estimate – Role Editing, Save, Version History & Restore

> Paste everything below the line into the coding agent. Defaults are chosen for every open decision (see §0.3); change them there if you disagree.

---

## ROLE
You are a senior full-stack engineer (Python 3.11, FastAPI, SQLAlchemy 2.x, SQL Server/T-SQL, plus the existing ClearOps frontend). Repo: `pankajktiwari6/clearops`. Make the **smallest correct change** that follows existing conventions. Do not refactor unrelated code. Do not touch Apply Template, Save Template, Forecast or WBS pages.

## 0. PRE-FLIGHT

### 0.1 Read first (mandatory)
- `ClearOps_App/app/models/project_estimator.py`, `schemas/project_estimator.py`, `models/mixins.py`
- `ClearOps_App/app/api/crud.py`, `core/database.py`, `main.py`
- `ClearOps_App/app/column_mapping.json` (frontend contract: every new table/field must be registered here)
- `clearops_microservices/services/project/service.py` and `common/domain.py` (the project service owns `ProjectEstimator`; new endpoints go here)
- Locate the frontend Project Estimate page. **If it is not in this repo, say so** and deliver backend + API contract + a precise frontend spec. Do not invent a UI framework.

### 0.2 Facts about the current code
- Existing main table: `gold.ProjectEstimator` (PK `Project_Estimater_Id`; columns `Task_ID, Job_title, Task_Name, QTY, HRS, Rate, Total, SubTotal, Task_Number, Project_Id, Parent_Task_ID, Delivery_Type, Resource_Id`).
- It uses `GoldControlColumnsMixin` (requires `SourceRowHash`, `PipelineRunId` – pipeline-fed). User-saved rows have no pipeline run: **make these columns nullable or populate them with a documented sentinel; do not break the pipeline loader.**
- The generic CRUD in `crud.py` has no transactional/versioned endpoints.

### 0.3 Decisions (defaults – state any deviation in the PR)
| # | Decision | Default |
|---|----------|---------|
| D1 | Main table name | **`gold.ProjectEstimator`** (existing). Do not create `gold.ClearOps_ProjectEstimator` unless the repo convention requires an application-owned `ClearOps_` table for user-written data. |
| D2 | Version storage | **Header + line child table** (two tables). |
| D3 | Restore semantics | **Flip the current pointer only**; history stays append-only; no "Restored" version created. |
| D4 | Main-table consistency on restore | **Rewrite main table to match the restored snapshot** (upsert/delete in the same transaction). |

## 1. CURRENT UI (from screenshots)
- Header: **Estimate Revenue**, **Estimate Project Cost**. Buttons: Collapse All Rows, Expand All Rows, **Version History**, Apply Template, Save Template, **Save Estimate**.
- Grid columns: Task Name, Task Number, Qty, Hrs, Rate, Total, Subtotal. A task row (e.g. `LABOR`, `01.Fee`) has an **Add Role** checkbox; ticked → role rows appear beneath.
- Role row: delete icon, **role dropdown** (e.g. "PR Digitl Social Strat Prof 4 - 15…"), editable **Qty / Hrs / Rate**, computed Total, and a `+ Add Role` row.
- Roles come from the rate schedule (banner: "CAN-Novo 2025 New (106 roles)").
- Banner: "You have unsaved changes on N role(s). Click Save to keep them."
- Legend: blue = Fusion Synced, green = Manually Created.

## 2. STEP 1 – ROLE EDITING (client-side draft only)
1. User selects a role from the dropdown and enters **integers** in Qty, Hrs, Rate.
   - Digits only (`^\d+$`); reject negative, decimal, empty, non-numeric. Qty ≥ 1, Hrs ≥ 0, Rate ≥ 0. Inline validation messages.
   - Pre-fill Rate from the selected role's rate-schedule rate; user may override.
2. `Total = Qty × Hrs × Rate`; task Subtotal = Σ role totals; Estimate Revenue = Σ subtotals. **Recompute on the server too – never trust client totals.**
3. **Known defect – fix with root cause + unit test:** `21 × 10 × 159` must be **$33,390**, but the screenshot shows **$3,358,080** (also propagated to subtotal and header). Find the cause (stale state / unparsed string / wrong multiplier).
4. **No persistence on change, blur or dropdown select.** Edits live in local draft state; track dirty roles; drive the unsaved-changes banner from it; warn on navigation while dirty.
5. Persist **only** when the user clicks **Save Estimate** (disable button + spinner while in flight; on failure keep the draft and show the error; on success clear dirty state and reload).

## 3. STEP 2 – SAVE (single atomic transaction)
**Endpoint:** `PUT /projectestimator/projects/{project_id}/estimate`
**Body:** `{ base_version_no: int|null, lines: [{task_id, task_number, task_name, job_title, resource_id?, qty, hrs, rate, delivery_type?}] }`

In **one transaction** (full rollback on any error):
1. **Validate:** project exists; `task_id`s belong to the project; integers in range; caller authorised for the project (identity from the Azure AD gateway token – never from the body).
2. **Optimistic check:** if `base_version_no` ≠ current version → **409**.
3. **Upsert main table:** update by key, insert new, delete removed rows. Recompute `Total`/`SubTotal` with `Decimal`. Stamp `GoldCreatedBy / GoldModifiedBy / GoldModifiedDate` from the authenticated user.
4. **Next version number:** `MAX(Version_No)+1` per project **under a lock** (`UPDLOCK, HOLDLOCK` or `sp_getapplock`). Per-project, starts at 1, never reused/renumbered.
5. **Insert** one version header + N version lines = **full snapshot** after the save (not a diff).
6. Set `Is_Current = 0` on previous versions and `1` on the new one.
7. **No-op save** (nothing changed) → create no version, return the current one.
8. **`Change_Summary`** (auto, ≤ 500 chars, matches screenshot style), joined by `; `:
   - `Updated hours of role 'PR Digitl Social Strat Prof 4' on LABOR LABOR`
   - `Updated quantity of role 'unassigned' on PASS THROUGH PASS THROUGH`
   - `Updated rate of role …` / `Added role …` / `Removed role …`
9. **Return:** `{ version_no, total_amount, line_count }`.

### 3.1 DDL (idempotent migration script; `IF OBJECT_ID(...) IS NULL`)
`gold.clearops_project_estimator_version` (header; application-owned → `GoldAuditColumnsMixin` only, no pipeline columns):

| Column | Type |
|---|---|
| Version_Id | BIGINT IDENTITY PK |
| Project_Id | BIGINT FK → gold.Project_Master |
| Version_No | INT NOT NULL |
| Total_Amount | DECIMAL(18,2) |
| Line_Count | INT |
| Change_Summary | NVARCHAR(500) |
| Is_Current | BIT NOT NULL DEFAULT 0 |
| Created_By | NVARCHAR(256) (user email) |
| Created_Date | DATETIME2 DEFAULT SYSUTCDATETIME() |
| + audit columns | per `GoldAuditColumnsMixin` |

Constraints: `UNIQUE (Project_Id, Version_No)`; **filtered unique index** `ON (Project_Id) WHERE Is_Current = 1` (≤ 1 current version per project).

`gold.clearops_project_estimator_version_line` (snapshot):
`Version_Line_Id PK`, `Version_Id FK`, `Project_Estimater_Id` (nullable soft ref), `Task_ID`, `Task_Number`, `Task_Name`, `Job_Title`, `Resource_Id`, `QTY`, `HRS`, `Rate`, `Total`, `SubTotal`, `Delivery_Type`; index on `Version_Id`.

> Alternative if a **single** table is required: `Snapshot_Json NVARCHAR(MAX)` with `CHECK (ISJSON(Snapshot_Json)=1)`. API contract must be identical either way.

Deliver: DDL script, SQLAlchemy models, Pydantic schemas (`Create/Update/Response/SortField` per existing pattern), and `column_mapping.json` entries.

## 4. STEP 3 – VERSION HISTORY POPUP
Button **Version History** opens modal **"Estimate Version History"**.

- **Left list** (scrollable, newest first, paged/lazy): `Version {n}`, red **Current** pill on the active one, total right-aligned (`$29,430`), change summary, then `{email} · {M/D/YYYY, h:mm:ss AM/PM}` (convert UTC → user local time).
- **Right detail** of the highlighted version: header `Version 88 · 3 role line(s) · $29,430`; table **Task | Role | Qty | Hours | Rate | Total**, e.g. `LABOR LABOR | PR Digitl Social Strat Prof 4 | 12 | 10 | 159 | $19,080`. Task rows with no role show `—` and `$0`.
- **Footer:** **Close** (red text) and **Restore This Version** (disabled/grey while the current or no version is selected).
- **Mobile (<~600px):** single-column list; tap opens detail; selected row highlighted light red.
- Accessibility: focus trap, Esc closes, `aria-selected` on the list.

**Endpoints**
- `GET /projectestimator/projects/{id}/versions?limit=&offset=` → list
- `GET /projectestimator/projects/{id}/versions/{version_no}` → lines

## 5. STEP 4 – SELECT VERSION → BECOMES CURRENT
- Clicking a list row **only previews** it; no data changes.
- **Restore This Version** → confirm dialog (warn about unsaved edits) → `POST /projectestimator/projects/{id}/versions/{version_no}/restore`.
- One transaction: set all `Is_Current = 0`, target `= 1`; **do not delete or rewrite history**; make the main table match the snapshot (D4); no new version row (D3).
- After success: close modal, reload grid, refresh header totals; **Current** pill moves to the restored version.
- Next **Save Estimate** after a restore creates `MAX(Version_No)+1` (not `restored+1`) and becomes current.

## 6. STEP 5 – READS FILTERED BY CURRENT VERSION
`GET /projectestimator/projects/{id}/estimate`
- **Current version exists** → return only that version's lines (join main table to `version_line` on `Project_Estimater_Id` where `Version_Id = current`, or read the snapshot directly).
- **No version yet** → normal flow: return main-table rows for the project unchanged. **Reads never create versions.**
- Header Estimate Revenue / Project Cost must come from the **same filtered set**. Never show a mix of two versions.

## 7. CROSS-CUTTING REQUIREMENTS
- **Security:** parameterised queries only; authorise every endpoint; user from gateway token; 403 on inaccessible `project_id`.
- **Concurrency:** race-safe version numbers (§3.4) + `base_version_no` → 409.
- **Money:** `Decimal` server-side, never float; 2-dp display with thousands separators.
- **Observability:** log project, version, user on save and restore.
- **Compatibility:** do not break existing generic CRUD routers or `column_mapping.json` consumers; do not break the pipeline loader of `gold.ProjectEstimator`.

## 8. TESTS (required – show passing output)
1. Edit without Save → no DB write; banner counts dirty roles.
2. Save → main-table rows + version N with correct totals and summary text.
3. No-op save → no new version.
4. Two concurrent saves → distinct consecutive versions, no duplicate-key error.
5. Invalid input (negative, decimal, text, empty) → rejected client-side and 422 server-side.
6. List endpoint ordered newest-first; exactly one `Is_Current = 1`.
7. Restore flips current atomically; filtered read returns exactly that snapshot.
8. Project with no versions → normal main-table data.
9. No access → 403; stale `base_version_no` → 409.
10. Regression: `21 × 10 × 159 = 33,390` renders correctly.

## 9. OUTPUT FORMAT
1. Short **plan**: files to change + any deviation from D1–D4.
2. Implementation.
3. Test results.
4. PR description (table-name decision, version-table design, restore semantics).
5. Commit on branch `claude/bold-mayer-4iyowp` and push. **Do not open a PR unless asked.**
6. If anything is ambiguous or contradicts the code, ask **one concise question** before implementing; do not guess silently.
