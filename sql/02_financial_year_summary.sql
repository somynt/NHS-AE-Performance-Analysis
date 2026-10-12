-- Q2. How have demand and performance changed year by year?
-- Complete NHS financial years only (April to March, 12 months of data).
-- Skills: JOIN, GROUP BY, HAVING, conditional aggregation

SELECT
    m.financial_year,
    SUM(a.att_total)                                                    AS attendances,
    SUM(a.att_type1)                                                    AS type1_attendances,
    SUM(a.adm_total)                                                    AS emergency_admissions,
    ROUND(100.0 * SUM(p.within4_total) / SUM(p.within4_total + p.over4_total), 1) AS pct_within_4h,
    ROUND(100.0 * SUM(p.within4_type1) / SUM(p.within4_type1 + p.over4_type1), 1) AS pct_within_4h_type1,
    SUM(a.dta_over_12hrs)                                               AS waits_over_12h_after_decision_to_admit,
    MAX(m.flag_estimated_from_weekly + m.flag_crs_field_test + m.flag_cyber_attack_type3) > 0 AS has_data_caveat
FROM dim_month m
JOIN fact_activity    a ON a.month_key = m.month_key
JOIN fact_performance p ON p.month_key = m.month_key
GROUP BY m.financial_year
HAVING COUNT(*) = 12
ORDER BY m.financial_year;
