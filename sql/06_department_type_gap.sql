-- Q6. How much worse is performance in major A&E (Type 1) than in minor units (Type 3)?
-- Skills: JOIN, aggregation by year, derived metric

SELECT
    m.year,
    ROUND(100.0 * SUM(p.within4_type1) / SUM(p.within4_type1 + p.over4_type1), 1) AS pct_within_4h_type1,
    ROUND(100.0 * SUM(p.within4_type3) / SUM(p.within4_type3 + p.over4_type3), 1) AS pct_within_4h_type3,
    ROUND(100.0 * SUM(p.within4_type3) / SUM(p.within4_type3 + p.over4_type3)
        - 100.0 * SUM(p.within4_type1) / SUM(p.within4_type1 + p.over4_type1), 1)  AS gap_points,
    ROUND(100.0 * SUM(a.att_type3) / SUM(a.att_total), 1)                          AS type3_share_of_attendances_pct
FROM dim_month m
JOIN fact_performance p ON p.month_key = m.month_key
JOIN fact_activity    a ON a.month_key = m.month_key
WHERE m.year BETWEEN 2011 AND 2025          -- complete calendar years only
GROUP BY m.year
ORDER BY m.year;
