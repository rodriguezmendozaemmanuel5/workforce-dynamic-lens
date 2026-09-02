-- =============================================================================
-- WORKFORCE DYNAMIC LENS — MODULE v0.6.0
-- Script 13: Power BI Analytical Layer (Views)
-- Engine Target: PostgreSQL 15+
-- Design Freeze Baseline: v1.0 (August 2026)
-- Author: Emmanuel Rodríguez Mendoza
-- =============================================================================

SET search_path TO people_analytics, public;

-- -----------------------------------------------------------------------------
-- View 1: Active Employees Current Snapshot
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW people_analytics.view_active_employees_current AS
SELECT 
    e.employee_sk,
    e.employee_id,
    e.first_name || ' ' || e.last_name AS full_name,
    e.work_email,
    e.gender,
    e.country_code,
    e.work_location_type,
    d.department_sk,
    d.department_name,
    d.region,
    p.position_sk,
    p.job_title,
    p.job_family,
    p.career_level,
    p.is_critical_position,
    e.hire_date,
    ROUND((CURRENT_DATE - e.hire_date) / 365.25, 2) AS tenure_years,
    e.annual_base_salary_usd,
    e.fully_loaded_cost_usd,
    e.performance_rating,
    e.potential_rating
FROM people_analytics.dim_employees e
JOIN people_analytics.dim_departments d ON e.department_sk = d.department_sk
JOIN people_analytics.dim_positions p ON e.position_sk = p.position_sk
WHERE e.is_current_row = TRUE 
  AND e.is_active = TRUE;

COMMENT ON VIEW people_analytics.view_active_employees_current IS 'Active employee master snapshot for headcount and demographics analytics';

-- -----------------------------------------------------------------------------
-- View 2: Monthly Attrition Summary (KPI-HR-01, KPI-FIN-01)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW people_analytics.view_monthly_attrition_summary AS
SELECT 
    d.year_number,
    d.month_number,
    d.year_month_label,
    t.termination_type,
    t.proxy_reclassified_reason,
    COUNT(t.termination_sk) AS termination_count,
    SUM(CASE WHEN t.is_regrettable_attrition THEN 1 ELSE 0 END) AS regrettable_count,
    SUM(t.severance_cost_usd) AS total_severance_cost_usd,
    ROUND(AVG(t.notice_period_days), 1) AS avg_notice_period_days
FROM people_analytics.fact_terminations t
JOIN people_analytics.dim_date d ON t.termination_date_sk = d.date_sk
GROUP BY d.year_number, d.month_number, d.year_month_label, t.termination_type, t.proxy_reclassified_reason;

COMMENT ON VIEW people_analytics.view_monthly_attrition_summary IS 'Monthly turnover aggregates by termination type, reclassified proxy reason, and financial severance impact';

-- -----------------------------------------------------------------------------
-- View 3: Bradford Scores Rolling 12 Months (KPI-OP-01)
-- Formula: B = S^2 * D (S = absence instances count, D = total absence days)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW people_analytics.view_bradford_scores_rolling_12m AS
WITH raw_absences AS (
    SELECT 
        al.employee_sk,
        COUNT(CASE WHEN al.is_absence_instance_start = TRUE THEN 1 END) AS total_instances_S,
        COUNT(al.attendance_sk) AS total_days_D
    FROM people_analytics.fact_attendance_logs al
    JOIN people_analytics.dim_date d ON al.date_sk = d.date_sk
    WHERE al.is_unplanned_absence = TRUE
      AND d.date_actual >= CURRENT_DATE - INTERVAL '12 months'
    GROUP BY al.employee_sk
)
SELECT 
    e.employee_sk,
    e.employee_id,
    e.first_name || ' ' || e.last_name AS full_name,
    d.department_name,
    COALESCE(ra.total_instances_S, 0) AS absence_instances_S,
    COALESCE(ra.total_days_D, 0) AS total_absence_days_D,
    (POWER(COALESCE(ra.total_instances_S, 0), 2) * COALESCE(ra.total_days_D, 0))::INTEGER AS bradford_score,
    CASE 
        WHEN (POWER(COALESCE(ra.total_instances_S, 0), 2) * COALESCE(ra.total_days_D, 0)) >= 500 THEN 'Critical Risk (500+)'
        WHEN (POWER(COALESCE(ra.total_instances_S, 0), 2) * COALESCE(ra.total_days_D, 0)) >= 200 THEN 'High Risk (200-499)'
        WHEN (POWER(COALESCE(ra.total_instances_S, 0), 2) * COALESCE(ra.total_days_D, 0)) >= 51  THEN 'Moderate Concern (51-199)'
        ELSE 'Normal Range (0-50)'
    END AS bradford_risk_tier
FROM people_analytics.dim_employees e
JOIN people_analytics.dim_departments d ON e.department_sk = d.department_sk
LEFT JOIN raw_absences ra ON e.employee_sk = ra.employee_sk
WHERE e.is_current_row = TRUE 
  AND e.is_active = TRUE;

COMMENT ON VIEW people_analytics.view_bradford_scores_rolling_12m IS 'Rolling 12-month Bradford Factor Scores (S^2 * D) per active employee for absenteeism risk assessment';

-- -----------------------------------------------------------------------------
-- View 4: Compa-Ratio by Employee (KPI-HR-02)
-- Formula: Compa-Ratio = Annual Salary USD / Market Midpoint USD
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW people_analytics.view_compa_ratio_by_employee AS
SELECT 
    e.employee_sk,
    e.employee_id,
    e.first_name || ' ' || e.last_name AS full_name,
    d.department_name,
    p.job_title,
    p.career_level,
    e.country_code,
    e.annual_base_salary_usd,
    b.market_min_salary_usd,
    b.market_midpoint_salary_usd,
    b.market_max_salary_usd,
    ROUND(e.annual_base_salary_usd / NULLIF(b.market_midpoint_salary_usd, 0), 4) AS compa_ratio,
    CASE 
        WHEN (e.annual_base_salary_usd / NULLIF(b.market_midpoint_salary_usd, 0)) < 0.85 THEN 'Underpaid (< 0.85)'
        WHEN (e.annual_base_salary_usd / NULLIF(b.market_midpoint_salary_usd, 0)) BETWEEN 0.85 AND 1.15 THEN 'Market Aligned (0.85 - 1.15)'
        WHEN (e.annual_base_salary_usd / NULLIF(b.market_midpoint_salary_usd, 0)) > 1.15 THEN 'Above Market (> 1.15)'
        ELSE 'No Benchmark Data'
    END AS compa_ratio_tier
FROM people_analytics.dim_employees e
JOIN people_analytics.dim_departments d ON e.department_sk = d.department_sk
JOIN people_analytics.dim_positions p ON e.position_sk = p.position_sk
LEFT JOIN people_analytics.dim_salary_benchmarks b 
       ON e.position_sk = b.position_sk 
      AND e.country_code = b.country_code
      AND b.is_current_benchmark = TRUE
WHERE e.is_current_row = TRUE 
  AND e.is_active = TRUE;

COMMENT ON VIEW people_analytics.view_compa_ratio_by_employee IS 'Individual Compa-Ratio calculations against current market salary benchmarks';

-- -----------------------------------------------------------------------------
-- View 5: SLA Penalty Attribution (KPI-FIN-02)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW people_analytics.view_sla_penalty_attribution AS
SELECT 
    d.department_sk,
    d.department_name,
    dt.year_number,
    dt.month_number,
    dt.year_month_label,
    se.shift_id,
    se.breach_type,
    se.attributed_to_staffing_deficit,
    COUNT(se.sla_event_sk) AS event_count,
    SUM(se.hours_delayed) AS total_hours_delayed,
    SUM(se.penalty_cost_usd) AS total_penalty_cost_usd
FROM people_analytics.fact_sla_events se
JOIN people_analytics.dim_departments d ON se.department_sk = d.department_sk
JOIN people_analytics.dim_date dt ON se.event_date_sk = dt.date_sk
GROUP BY d.department_sk, d.department_name, dt.year_number, dt.month_number, dt.year_month_label, se.shift_id, se.breach_type, se.attributed_to_staffing_deficit;

COMMENT ON VIEW people_analytics.view_sla_penalty_attribution IS 'SLA penalty costs aggregated by department, breach type, and staffing deficit attribution';

-- -----------------------------------------------------------------------------
-- View 6: Total Cost of Attrition (KPI-FIN-01, KPI-EXEC-02)
-- Severance + Estimated Replacement Cost Proxy (1.5x Annual Salary for Critical, 0.5x for Non-Critical)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW people_analytics.view_total_cost_of_attrition AS
SELECT 
    dt.year_number,
    dt.month_number,
    dt.year_month_label,
    d.department_name,
    t.termination_type,
    COUNT(t.termination_sk) AS separations_count,
    SUM(t.severance_cost_usd) AS direct_severance_cost_usd,
    SUM(
        CASE 
            WHEN p.is_critical_position = TRUE THEN e.annual_base_salary_usd * 1.50
            ELSE e.annual_base_salary_usd * 0.50
        END
    ) AS estimated_replacement_cost_usd,
    SUM(t.severance_cost_usd) + SUM(
        CASE 
            WHEN p.is_critical_position = TRUE THEN e.annual_base_salary_usd * 1.50
            ELSE e.annual_base_salary_usd * 0.50
        END
    ) AS total_attrition_financial_impact_usd
FROM people_analytics.fact_terminations t
JOIN people_analytics.dim_employees e ON t.employee_sk = e.employee_sk
JOIN people_analytics.dim_departments d ON e.department_sk = d.department_sk
JOIN people_analytics.dim_positions p ON e.position_sk = p.position_sk
JOIN people_analytics.dim_date dt ON t.termination_date_sk = dt.date_sk
GROUP BY dt.year_number, dt.month_number, dt.year_month_label, d.department_name, t.termination_type;

COMMENT ON VIEW people_analytics.view_total_cost_of_attrition IS 'Comprehensive financial cost of turnover including severance and position replacement proxies';

-- -----------------------------------------------------------------------------
-- View 7: High Performer Retention (KPI-EXEC-01)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW people_analytics.view_high_performer_retention AS
SELECT 
    e.employee_sk,
    e.employee_id,
    e.first_name || ' ' || e.last_name AS full_name,
    d.department_name,
    p.job_title,
    p.is_critical_position,
    e.performance_rating,
    e.potential_rating,
    e.is_active,
    t.termination_date,
    t.termination_type,
    t.proxy_reclassified_reason,
    t.is_regrettable_attrition
FROM people_analytics.dim_employees e
JOIN people_analytics.dim_departments d ON e.department_sk = d.department_sk
JOIN people_analytics.dim_positions p ON e.position_sk = p.position_sk
LEFT JOIN people_analytics.fact_terminations t ON e.employee_sk = t.employee_sk
WHERE e.is_current_row = TRUE
  AND (e.performance_rating >= 4.00 
   OR e.potential_rating IN ('Alto', 'Top Talent'));

COMMENT ON VIEW people_analytics.view_high_performer_retention IS 'Tracking cohort for High Performers and Top Talent retention and regrettable attrition';
