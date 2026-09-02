-- =============================================================================
-- WORKFORCE DYNAMIC LENS — MODULE v0.6.0
-- Script 14: Post-Implementation Validation & Sanity Test Queries
-- Engine Target: PostgreSQL 15+
-- Design Freeze Baseline: v1.0 (August 2026)
-- Author: Emmanuel Rodríguez Mendoza
-- =============================================================================

SET search_path TO people_analytics, public;

-- =============================================================================
-- TEST SUITE 1: Table Structure & Row Count Baseline
-- =============================================================================
SELECT 'dim_date' AS table_name, COUNT(*) AS row_count FROM people_analytics.dim_date
UNION ALL
SELECT 'dim_departments', COUNT(*) FROM people_analytics.dim_departments
UNION ALL
SELECT 'dim_positions', COUNT(*) FROM people_analytics.dim_positions
UNION ALL
SELECT 'dim_salary_benchmarks', COUNT(*) FROM people_analytics.dim_salary_benchmarks
UNION ALL
SELECT 'dim_employees', COUNT(*) FROM people_analytics.dim_employees
UNION ALL
SELECT 'fact_attendance_logs', COUNT(*) FROM people_analytics.fact_attendance_logs
UNION ALL
SELECT 'fact_terminations', COUNT(*) FROM people_analytics.fact_terminations
UNION ALL
SELECT 'fact_sla_events', COUNT(*) FROM people_analytics.fact_sla_events
UNION ALL
SELECT 'stg_quarantine_records', COUNT(*) FROM people_analytics.stg_quarantine_records
UNION ALL
SELECT 'etl_load_history', COUNT(*) FROM people_analytics.etl_load_history;

-- =============================================================================
-- TEST SUITE 2: Foreign Key Referential Integrity (Orphan Detection)
-- All queries should return ZERO rows.
-- =============================================================================

-- 2.1 dim_employees -> dim_departments
SELECT 'Orphan Dept in Employees' AS test_name, COUNT(*) AS orphan_count
FROM people_analytics.dim_employees e
LEFT JOIN people_analytics.dim_departments d ON e.department_sk = d.department_sk
WHERE d.department_sk IS NULL;

-- 2.2 dim_employees -> dim_positions
SELECT 'Orphan Pos in Employees' AS test_name, COUNT(*) AS orphan_count
FROM people_analytics.dim_employees e
LEFT JOIN people_analytics.dim_positions p ON e.position_sk = p.position_sk
WHERE p.position_sk IS NULL;

-- 2.3 fact_attendance_logs -> dim_employees
SELECT 'Orphan Emp in Attendance' AS test_name, COUNT(*) AS orphan_count
FROM people_analytics.fact_attendance_logs al
LEFT JOIN people_analytics.dim_employees e ON al.employee_sk = e.employee_sk
WHERE e.employee_sk IS NULL;

-- 2.4 fact_attendance_logs -> dim_date
SELECT 'Orphan Date in Attendance' AS test_name, COUNT(*) AS orphan_count
FROM people_analytics.fact_attendance_logs al
LEFT JOIN people_analytics.dim_date d ON al.date_sk = d.date_sk
WHERE d.date_sk IS NULL;

-- 2.5 fact_terminations -> dim_employees
SELECT 'Orphan Emp in Terminations' AS test_name, COUNT(*) AS orphan_count
FROM people_analytics.fact_terminations t
LEFT JOIN people_analytics.dim_employees e ON t.employee_sk = e.employee_sk
WHERE e.employee_sk IS NULL;

-- 2.6 fact_sla_events -> dim_departments
SELECT 'Orphan Dept in SLA Events' AS test_name, COUNT(*) AS orphan_count
FROM people_analytics.fact_sla_events se
LEFT JOIN people_analytics.dim_departments d ON se.department_sk = d.department_sk
WHERE d.department_sk IS NULL;

-- =============================================================================
-- TEST SUITE 3: Grain & Uniqueness Integrity
-- All queries should return ZERO rows.
-- =============================================================================

-- 3.1 SCD2: Only ONE active row per employee_id
SELECT employee_id, COUNT(*) AS active_rows_count
FROM people_analytics.dim_employees
WHERE is_current_row = TRUE
GROUP BY employee_id
HAVING COUNT(*) > 1;

-- 3.2 Attendance Fact: Only ONE log per employee_sk per date_key
SELECT employee_sk, date_key, COUNT(*) AS duplicate_logs_count
FROM people_analytics.fact_attendance_logs
GROUP BY employee_sk, date_key
HAVING COUNT(*) > 1;

-- 3.3 Terminations Fact: Only ONE termination per employee_sk per termination_date
SELECT employee_sk, termination_date, COUNT(*) AS duplicate_trm_count
FROM people_analytics.fact_terminations
GROUP BY employee_sk, termination_date
HAVING COUNT(*) > 1;

-- 3.4 Benchmarks: Only ONE active benchmark per position + country
SELECT position_sk, country_code, COUNT(*) AS active_bmk_count
FROM people_analytics.dim_salary_benchmarks
WHERE is_current_benchmark = TRUE
GROUP BY position_sk, country_code
HAVING COUNT(*) > 1;

-- =============================================================================
-- TEST SUITE 4: Analytical Views Compilation & Execution Verification
-- Each query executes a LIMIT 5 on the views.
-- =============================================================================
SELECT * FROM people_analytics.view_active_employees_current LIMIT 5;
SELECT * FROM people_analytics.view_monthly_attrition_summary LIMIT 5;
SELECT * FROM people_analytics.view_bradford_scores_rolling_12m LIMIT 5;
SELECT * FROM people_analytics.view_compa_ratio_by_employee LIMIT 5;
SELECT * FROM people_analytics.view_sla_penalty_attribution LIMIT 5;
SELECT * FROM people_analytics.view_total_cost_of_attrition LIMIT 5;
SELECT * FROM people_analytics.view_high_performer_retention LIMIT 5;

-- =============================================================================
-- TEST SUITE 5: Business Rule Consistency (Termination ↔ Employment State)
-- All queries should return ZERO rows.
-- =============================================================================

-- 5.1 Active current employees who have a termination event (R04 violation)
SELECT 'Active Emp with Termination' AS test_name, COUNT(*) AS violation_count
FROM people_analytics.dim_employees e
JOIN people_analytics.fact_terminations t ON e.employee_sk = t.employee_sk
WHERE e.is_current_row = TRUE
  AND e.is_active = TRUE;

-- 5.2 Inactive current employees without a termination event (R05 violation)
SELECT 'Inactive Emp without Termination' AS test_name, COUNT(*) AS violation_count
FROM people_analytics.dim_employees e
LEFT JOIN people_analytics.fact_terminations t ON e.employee_sk = t.employee_sk
WHERE e.is_current_row = TRUE
  AND e.is_active = FALSE
  AND t.termination_sk IS NULL;

-- 5.3 Termination date before hire date (R07 violation)
SELECT 'Termination Before Hire' AS test_name, COUNT(*) AS violation_count
FROM people_analytics.fact_terminations t
JOIN people_analytics.dim_employees e ON t.employee_sk = e.employee_sk
WHERE e.is_current_row = TRUE
  AND t.termination_date < e.hire_date;

-- 5.4 Multiple current SCD2 rows per employee (R08 violation)
SELECT 'Multiple Current Rows' AS test_name, COUNT(*) AS violation_count
FROM (
    SELECT employee_id, COUNT(*) AS cnt
    FROM people_analytics.dim_employees
    WHERE is_current_row = TRUE
    GROUP BY employee_id
    HAVING COUNT(*) > 1
) dupes;

-- 5.5 SCD2 overlapping periods (R10 violation)
SELECT 'SCD2 Overlapping Periods' AS test_name, COUNT(*) AS violation_count
FROM people_analytics.dim_employees e1
JOIN people_analytics.dim_employees e2
  ON e1.employee_id = e2.employee_id
  AND e1.employee_sk < e2.employee_sk
  AND e1.row_effective_date < e2.row_expiration_date
  AND e2.row_effective_date < e1.row_expiration_date;

-- 5.6 Attendance after termination date (R11 / R15 violation)
SELECT 'Ghost Attendance Records' AS test_name, COUNT(*) AS violation_count
FROM people_analytics.fact_attendance_logs al
JOIN people_analytics.dim_employees e ON al.employee_sk = e.employee_sk
JOIN people_analytics.fact_terminations t ON e.employee_sk = t.employee_sk
WHERE e.is_current_row = TRUE
  AND al.date_key > t.termination_date;

-- 5.7 Headcount consistency check
SELECT 
    'Headcount Check' AS test_name,
    (SELECT COUNT(*) FROM people_analytics.dim_employees WHERE is_current_row = TRUE AND is_active = TRUE) AS active_headcount,
    (SELECT COUNT(*) FROM people_analytics.dim_employees WHERE is_current_row = TRUE AND is_active = FALSE) AS inactive_headcount,
    (SELECT COUNT(*) FROM people_analytics.dim_employees WHERE is_current_row = TRUE) AS total_current_rows,
    (SELECT COUNT(DISTINCT employee_id) FROM people_analytics.dim_employees) AS unique_employees,
    (SELECT COUNT(*) FROM people_analytics.fact_terminations) AS termination_count;
