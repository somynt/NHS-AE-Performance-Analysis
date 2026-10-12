-- Q4. Which months had the worst 4-hour performance in major (Type 1) A&E?
-- Skills: CTE, RANK window function, filtering on a ranked result

WITH ranked AS (
    SELECT
        m.month_label,
        m.season,
        ROUND(100.0 * p.within4_type1 / (p.within4_type1 + p.over4_type1), 1) AS pct_within_4h_type1,
        p.over4_type1                                                          AS type1_patients_over_4h,
        RANK() OVER (ORDER BY 1.0 * p.within4_type1 / (p.within4_type1 + p.over4_type1)) AS worst_rank
    FROM dim_month m
    JOIN fact_performance p ON p.month_key = m.month_key
)
SELECT *
FROM ranked
WHERE worst_rank <= 10
ORDER BY worst_rank;
