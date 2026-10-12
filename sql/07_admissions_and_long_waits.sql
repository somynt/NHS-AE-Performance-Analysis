-- Q7. Are more patients being admitted, and how long do they wait for a bed?
-- 12-hour "trolley waits" = patients waiting over 12 hours from the decision
-- to admit them until they actually got a bed.
-- Skills: JOIN, GROUP BY, LAG for year-on-year growth, NULLIF to avoid divide-by-zero

WITH yearly AS (
    SELECT
        m.financial_year,
        SUM(a.att_type1)        AS type1_attendances,
        SUM(a.adm_via_type1)    AS admitted_via_type1,
        SUM(a.dta_over_4hrs)    AS waits_over_4h_for_bed,
        SUM(a.dta_over_12hrs)   AS waits_over_12h_for_bed
    FROM dim_month m
    JOIN fact_activity a ON a.month_key = m.month_key
    GROUP BY m.financial_year
    HAVING COUNT(*) = 12
)
SELECT
    financial_year,
    type1_attendances,
    ROUND(100.0 * admitted_via_type1 / type1_attendances, 1)           AS type1_admission_rate_pct,
    waits_over_4h_for_bed,
    waits_over_12h_for_bed,
    ROUND(100.0 * waits_over_12h_for_bed / admitted_via_type1, 2)      AS pct_admitted_waiting_over_12h,
    ROUND(1.0 * waits_over_12h_for_bed
          / NULLIF(LAG(waits_over_12h_for_bed) OVER (ORDER BY financial_year), 0), 1) AS times_previous_year
FROM yearly
ORDER BY financial_year;
