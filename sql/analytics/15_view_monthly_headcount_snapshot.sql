-- =============================================================================
-- Workforce Dynamic Lens -- v0.7.1 Power BI Model Support
-- View: view_monthly_headcount_snapshot
--
-- Purpose:
--   Provides point-in-time monthly headcount derived directly from SCD2
--   row_effective_date / row_expiration_date in dim_employees.
--   Used as the denominator for SHRM-aligned Annualized Turnover Rate in
--   Power BI, replacing the estimation-based Avg Headcount formula.
--
-- Methodology:
--   For each month M, an employee is counted if they were active on the
--   first day of that month:
--       row_effective_date <= month_start AND row_expiration_date >= month_start
--
-- Scope: 2020-01 to 2025-12 (72 months -- aligned with MonthlyAttrition)
-- =============================================================================

CREATE OR REPLACE VIEW people_analytics.view_monthly_headcount_snapshot AS
WITH months AS (
    SELECT
        generate_series(
            '2020-01-01'::date,
            '2025-12-31'::date,
            '1 month'::interval
        )::date AS month_start
)
SELECT
    to_char(m.month_start, 'YYYY-MM')           AS year_month_label,
    EXTRACT(YEAR  FROM m.month_start)::SMALLINT  AS year_number,
    EXTRACT(MONTH FROM m.month_start)::SMALLINT  AS month_number,
    m.month_start                                AS month_start_date,
    COUNT(e.employee_sk)                         AS headcount_snapshot
FROM months m
JOIN people_analytics.dim_employees e
    ON  e.row_effective_date <= m.month_start
    AND e.row_expiration_date >= m.month_start
LEFT JOIN people_analytics.fact_terminations t
    ON  e.employee_sk = t.employee_sk
WHERE (t.termination_date IS NULL OR t.termination_date >= m.month_start)
GROUP BY m.month_start
ORDER BY m.month_start;

COMMENT ON VIEW people_analytics.view_monthly_headcount_snapshot IS
'Point-in-time monthly active headcount snapshot derived from SCD2 periods and fact_terminations offboarding dates. SHRM denominator for Annualized Turnover Rate in Power BI. v0.7.0.';
