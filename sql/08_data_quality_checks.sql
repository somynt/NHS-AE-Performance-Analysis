-- Q8. Data quality checks before trusting any of the above.
-- Skills: reconciliation checks, LEFT JOIN to find missing rows, COUNT with CASE

SELECT 'Months in activity table'                         AS check_name, COUNT(*) AS result FROM fact_activity
UNION ALL
SELECT 'Months with activity but no 4-hour data',
       COUNT(*) FROM fact_activity a LEFT JOIN fact_performance p ON p.month_key = a.month_key
       WHERE p.month_key IS NULL
UNION ALL
SELECT 'Months where type totals do not match overall total (>5 patients)',
       COUNT(*) FROM fact_activity WHERE ABS(att_type1 + att_type2 + att_type3 - att_total) > 5
UNION ALL
SELECT 'Months where 4-hour counts do not equal total attendances (>5 patients)',
       COUNT(*) FROM fact_activity a JOIN fact_performance p ON p.month_key = a.month_key
       WHERE ABS(p.within4_total + p.over4_total - a.att_total) > 5
UNION ALL
SELECT 'Months estimated from weekly data',          SUM(flag_estimated_from_weekly) FROM dim_month
UNION ALL
SELECT 'Months affected by CRS field test',          SUM(flag_crs_field_test)        FROM dim_month
UNION ALL
SELECT 'Months affected by Type 3 cyber-attack gap', SUM(flag_cyber_attack_type3)    FROM dim_month;
