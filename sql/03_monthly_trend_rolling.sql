-- Q3. What is the underlying trend once month-to-month noise is smoothed out?
-- Skills: window functions (moving average with ROWS BETWEEN), LEFT JOIN

SELECT
    m.month_start,
    m.month_label,
    a.att_total,
    ROUND(AVG(a.att_total) OVER (ORDER BY m.month_key ROWS BETWEEN 11 PRECEDING AND CURRENT ROW), 0)
                                                                         AS att_total_12m_avg,
    ROUND(100.0 * p.within4_total / (p.within4_total + p.over4_total), 2) AS pct_within_4h,
    ROUND(100.0 * SUM(p.within4_total) OVER w / SUM(p.within4_total + p.over4_total) OVER w, 2)
                                                                         AS pct_within_4h_12m,
    ROUND(100.0 * p.within4_type1 / (p.within4_type1 + p.over4_type1), 2) AS pct_within_4h_type1,
    a.dta_over_12hrs,
    m.flag_estimated_from_weekly,
    m.flag_crs_field_test,
    m.flag_cyber_attack_type3,
    m.flag_covid_period
FROM dim_month m
JOIN fact_activity         a ON a.month_key = m.month_key
LEFT JOIN fact_performance p ON p.month_key = m.month_key
WINDOW w AS (ORDER BY m.month_key ROWS BETWEEN 11 PRECEDING AND CURRENT ROW)
ORDER BY m.month_key;
