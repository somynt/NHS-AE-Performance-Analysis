-- Q1. How did the latest month compare with the same month a year earlier?
-- Skills: JOIN, window function (LAG over 12 months), percentage change

WITH monthly AS (
    SELECT
        m.month_key,
        m.month_label,
        a.att_total,
        a.att_type1,
        a.adm_total,
        a.dta_over_12hrs,
        ROUND(100.0 * p.within4_total / (p.within4_total + p.over4_total), 1)  AS pct_within_4h,
        ROUND(100.0 * p.within4_type1 / (p.within4_type1 + p.over4_type1), 1)  AS pct_within_4h_type1
    FROM dim_month m
    JOIN fact_activity    a ON a.month_key = m.month_key
    JOIN fact_performance p ON p.month_key = m.month_key
),
with_last_year AS (
    SELECT
        *,
        LAG(month_label,         12) OVER (ORDER BY month_key) AS ly_month,
        LAG(att_total,           12) OVER (ORDER BY month_key) AS ly_att_total,
        LAG(adm_total,           12) OVER (ORDER BY month_key) AS ly_adm_total,
        LAG(dta_over_12hrs,      12) OVER (ORDER BY month_key) AS ly_dta_over_12hrs,
        LAG(pct_within_4h,       12) OVER (ORDER BY month_key) AS ly_pct_within_4h,
        LAG(pct_within_4h_type1, 12) OVER (ORDER BY month_key) AS ly_pct_within_4h_type1
    FROM monthly
)
SELECT
    month_label,
    ly_month                                                        AS compared_with,
    att_total,
    ROUND(100.0 * (att_total - ly_att_total) / ly_att_total, 1)     AS att_change_pct,
    adm_total,
    ROUND(100.0 * (adm_total - ly_adm_total) / ly_adm_total, 1)     AS adm_change_pct,
    pct_within_4h,
    ROUND(pct_within_4h - ly_pct_within_4h, 1)                      AS pct_4h_change_points,
    pct_within_4h_type1,
    ROUND(pct_within_4h_type1 - ly_pct_within_4h_type1, 1)          AS pct_4h_type1_change_points,
    dta_over_12hrs,
    ly_dta_over_12hrs
FROM with_last_year
ORDER BY month_key DESC
LIMIT 1;
