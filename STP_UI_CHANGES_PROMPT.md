# STP UI Changes: Eyeball Popup and Forecast Grid

**Context:** ClearOps Strategic Time Planner (STP). Two changes are needed: the resource "eyeball" popup, and the STP forecast grid. Before editing, find the relevant components in the repo and read how they currently render. Match the existing code style, tokens and components.

---

## 1. STP eyeball popup (resource allocation popup)

### Current state
- The popup title is the resource name (e.g. "Abha Mehta"), with the subtitle "Allocation on every project, by month".
- A green-boxed header strip shows **HRID, Job title, Job code, Standard hours / week, Budget % Productive**.
- A separate "On this task (...)" block (red-boxed) shows **Actuals (Project Timecard)**, **Budget (Estimate × Rate Card)** and **Future Forecast** (hrs and CA$).
- Below that is the month grid: Project, then Oct 2026, Nov 2026 and so on.
- The grid has a "Total planned · allocation" row and a "Capacity (Standard Hours/Week)" row.
- A footnote under the grid explains the data sources.

### Required changes
1. **Leave the green header strip unchanged.** Keep the same fields, labels, values and styling: HRID, Job title, Job code, Standard hours / week, Budget % Productive.
2. **Remove the red "On this task" block** as a separate section above the grid.
3. **Move its three values into the grid as fixed columns** between the **Project** column and the first month column. Use the order **Actuals | Budget | Future Forecast | Oct 2026 | Nov 2026 | ...**.
   - Actuals = Project Timecard hours for this resource on this project.
   - Budget = Estimate × Rate Card.
   - Future Forecast = forecast hours, with the currency amount underneath (e.g. `304 hrs` / `CA$36,480.00`).
   - Keep the empty-state text for the zero cases ("No Project Timecard hours for this resource on task 1.", "This task has no Project Estimate lines."). Show it as a tooltip or a muted "–" in the cell. Don't let it break row height.
4. **Make Project, Actuals, Budget and Future Forecast sticky (frozen).** Only the month columns scroll horizontally. Give the sticky columns a right-edge shadow or border and a solid background, so scrolling months never slides under them.
5. **Apply the same columns to every row.** This includes the "This project" row and any other project rows.
   - On the "Total planned · allocation" row, show the sums.
   - On the "Capacity" row, show "–" in these columns.
6. Keep the existing month-cell colouring (green intensity and % of capacity), the capacity row and the footnote.
7. Do the same for the older "Planned hours by project and month" eyeball popup if it is still reachable (e.g. "Khatri, Nitu – Vendor Consultant"). Keep one consistent layout.

---

## 2. STP forecast screen

### a) Don't block over-allocation
- The user must be able to enter hours that exceed the resource's remaining availability. Remove any clamping, hard validation or disabled save tied to this.
- Currently the input shows a red border with the message "Only 33.33 h left for Aadya Kush in Oct 2026".
- Keep this as a **non-blocking warning only**: the value stays as typed, Save forecast stays enabled, and the over-allocation is visible but doesn't stop the user.

### b) Replace the hover-only availability dots with always-visible indicators
- Use the "Resource forecast" layout from the reference screenshot (the one with the green arrows).
- Each month cell shows the hours input, plus a small **inline chip** beside or inside the cell showing availability. Examples are `7h free`, `59h over` and `94h free`.
- **Colour the cell border and chip by status:**
  - Available (utilisation below 80%): green.
  - Near capacity (80–100%): amber.
  - Over-allocated: red.
- Include the small legend ("Availability (all projects): Available <80% · Near capacity 80–100% · Over-allocated") above the grid.
- No hover is needed to read availability. Optionally keep a tooltip for the detailed breakdown.

### c) Fix row alignment
- In every row (resource, labor, pass-through), all inputs must be **the same height, baseline and vertical centre as the Rate input**. This covers the rate text box, each month's hours text box and the forecast total cells.
- Use one shared input style: the same height, border radius, padding, font size and text alignment.
- Column headers, values and chips must line up across rows. Month cells should be the same width on every row.
- Don't let the warning text or chip change the row height. Reserve a fixed slot for the chip so rows don't jump.

---

## Acceptance checks
- The green header fields are visually and functionally unchanged.
- The Actuals, Budget and Future Forecast columns sit between Project and the months and stay fixed while scrolling.
- The red "On this task" block no longer appears above the grid.
- Entering hours above availability saves successfully and shows a visible over-allocation chip and red styling.
- The availability status is readable without hovering.
- The Rate and hours inputs are aligned and equal in height on every row.
- Run the existing tests, lint and typecheck. Then launch the app and take before/after screenshots of both screens.

## Open questions
- Are the 80% / 100% thresholds correct for the availability colours?
- Should "Budget" in the new column show hours, currency or both?
