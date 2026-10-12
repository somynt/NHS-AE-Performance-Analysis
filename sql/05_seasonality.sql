-- Q5. Is there a seasonal pattern? Average by calendar month.
-- Uses the four most recent complete financial years so the pattern reflects
-- today's NHS, not 2010.
-- Skills: subquery, GROUP BY, CASE

WITH recent AS (
    SELECT m.*, a.att_total, a.att_type1, a.dta_over_12hrs,
           1.0 * p.within4_type1 / (p.within4_type1 + p.over4_type1) AS share_within_4h_type1
    FROM dim_month m
    JOIN fact_activity    a ON a.month_key = m.month_key
    JOIN fact_performance p ON p.month_key = m.month_key
    WHERE m.financial_year IN (
        SELECT financial_year FROM dim_month
        GROUP BY financial_year HAVING COUNT(*) = 12
        ORDER BY financial_year DESC LIMIT 4
    )
)
SELECT
    month_num,
    month_name,
    season,
    ROUND(AVG(att_total), 0)                 AS avg_attendances,
    ROUND(AVG(att_total) / (CASE WHEN month_num IN (4,6,9,11) THEN 30
                                 WHEN month_num = 2 THEN 28.25 ELSE 31 END), 0) AS avg_attendances_per_day,
    ROUND(100.0 * AVG(share_within_4h_type1), 1) AS avg_pct_within_4h_type1,
    ROUND(AVG(dta_over_12hrs), 0)            AS avg_waits_over_12h
FROM recent
GROUP BY month_num, month_name, season
ORDER BY month_num;
