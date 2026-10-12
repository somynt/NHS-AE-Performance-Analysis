# Power BI dashboard: build guide

Build time: about an hour in **Power BI Desktop** (free, Windows). When it's done, save the file as `powerbi/NHS_AE_Dashboard.pbix`, export a screenshot of each page to `powerbi/screenshots/`, and commit both through GitHub Desktop.

---

## 1. Load the data

1. **Home → Get data → Text/CSV** and load these four files from `data/clean/`:
   `dim_month.csv`, `fact_activity.csv`, `fact_performance.csv`, `fact_booked.csv`
2. For each file click **Transform Data** first and check:
   - `month_start` in `dim_month` is type **Date**
   - all count columns are **Whole number**
   - the `flag_` columns are **Whole number**
3. **Close & Apply**.

## 2. Build the data model (star schema)

In **Model view**:

1. Create relationships from `dim_month[month_key]` to `month_key` in each fact table:
   - Cardinality: **One to one** is what Power BI may suggest, because each fact table has one row per month. Change it to **One to many** (dim_month on the "one" side) so the model behaves like a standard star schema.
   - Cross-filter direction: **Single** (dim_month filters the facts)
2. Select `dim_month` → **Table tools → Mark as date table** → choose `month_start`.
3. Select `dim_month[month_name]` → **Column tools → Sort by column → month_num**, so months sort Jan to Dec instead of alphabetically.
4. Hide the `month_key` columns in the three fact tables (right-click → Hide in report view), so report builders always use the dimension.

**Interview point:** this is a star schema with one dimension (month) and three fact tables. Filters flow from the dimension to the facts, which keeps measures simple and stops double counting.

## 3. Add the measures

1. **Home → Enter data**, name the table `_Measures`, click **Load**.
2. Copy each measure from [`measures.dax`](measures.dax) and add it with **Home → New measure** (the `_Measures` table selected).
3. Format:
   - percentages (`% Within 4h`, `% Within 4h Type 1`, `Type 1 Admission Rate`, `Attendances vs LY %` and the rolling measure) → **Percentage, 1 decimal**
   - counts → **Whole number with thousands separator**
   - `(pts)` measures → **Decimal number, 1 decimal**
4. Delete the empty column Power BI created in `_Measures`. The table moves to the top of the Fields list.

**Interview point:** percentages are calculated as *sum of patients within 4 hours ÷ sum of all patients*, never as an average of monthly percentages. Averaging percentages gives quiet months the same weight as busy ones.

## 4. Page 1: Overview

| Visual | Fields |
|---|---|
| **Card** | `Latest Month` |
| **Card** | `Attendances Latest Month` (title: "Attendances") |
| **Card** | `% Within 4h Type 1 Latest Month` (title: "Seen within 4h, major A&E") |
| **Card** | `Type 1 Change vs LY (pts)` (title: "Change vs same month last year, points") |
| **Card** | `12h Waits Latest Month` (title: "Waited 12h+ for a bed") |
| **Line chart** | X: `dim_month[month_start]`; Y: `% Within 4h`, `% Within 4h Type 1`. Then **Analytics pane → Constant line** at 0.95, labelled "95% standard" |
| **Clustered column chart** | X: `dim_month[financial_year]`; Y: `Total Attendances` |
| **Slicer** | `dim_month[financial_year]` (dropdown) |

Add a small text box: *"Source: NHS England Monthly A&E Time Series, Sep 2026. Open Government Licence v3.0."*

## 5. Page 2: Seasonality

| Visual | Fields |
|---|---|
| **Matrix** | Rows: `financial_year`; Columns: `month_name`; Values: `% Within 4h Type 1` |
| Conditional formatting | Values → **Background colour → Gradient**, red (low) to green (high) |
| **Clustered column chart** | X: `month_name`; Y: `% Within 4h Type 1`; filter (Filters pane) `financial_year` to 2022-23 … 2025-26 |

**What to look for:** December and January are consistently the worst months; summer is the best.

## 6. Page 3: Long waits for a bed

| Visual | Fields |
|---|---|
| **Clustered column chart** | X: `financial_year`; Y: `12h Waits for a Bed` |
| **Line chart** | X: `financial_year`; Y: `Type 1 Admission Rate` |
| **Card** | `Data Caveat Note` (word wrap on) |

## 7. Page 4: Data notes

A text box with the four caveats from the README: estimated months (2010–2015), the CRS field test (2019–2023), booked appointments (from Aug 2020) and the Type 3 cyber-attack shortfall (Aug 2022–Feb 2023).

## 8. Finish

- **View → Themes**: pick one theme and keep colours consistent (e.g. Type 1 always the same colour).
- Give every visual a clear title saying what it shows, not just the field name.
- **File → Save as** `powerbi/NHS_AE_Dashboard.pbix`.
- **File → Export → Export to PDF**, or take screenshots of each page, and save to `powerbi/screenshots/`.
- Commit and push with GitHub Desktop, then add a screenshot to the README.

## Check your numbers

Your cards should match the SQL and Excel results for September 2026:

| Measure | Expected |
|---|---|
| Attendances Latest Month | 2,444,743 |
| % Within 4h Type 1 Latest Month | 60.6% |
| Type 1 Change vs LY (pts) | -0.5 |
| 12h Waits Latest Month | 50,582 |
| `% Within 4h Type 1` for 2025-26 (slicer) | 60.9% |
