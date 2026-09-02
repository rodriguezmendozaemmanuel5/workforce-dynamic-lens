-- =============================================================================
-- WORKFORCE DYNAMIC LENS — MODULE v0.6.0
-- Script 12: B-Tree & Partial Indexes Strategy
-- Engine Target: PostgreSQL 15+
-- Design Freeze Baseline: v1.0 (August 2026)
-- Author: Emmanuel Rodríguez Mendoza
-- =============================================================================

SET search_path TO people_analytics, public;

-- 1. dim_date Indexes
CREATE INDEX IF NOT EXISTS idx_dim_date_year_month
    ON people_analytics.dim_date (year_number, month_number);

-- 2. dim_employees Indexes & Partial Unique Index (SCD2)
CREATE UNIQUE INDEX IF NOT EXISTS uq_dim_emp_current_nk
    ON people_analytics.dim_employees (employee_id)
    WHERE is_current_row = TRUE;

CREATE INDEX IF NOT EXISTS idx_dim_emp_dept_active
    ON people_analytics.dim_employees (department_sk, is_active);

CREATE INDEX IF NOT EXISTS idx_dim_emp_position
    ON people_analytics.dim_employees (position_sk);

CREATE INDEX IF NOT EXISTS idx_dim_emp_perf_active
    ON people_analytics.dim_employees (performance_rating)
    WHERE is_active = TRUE;

CREATE INDEX IF NOT EXISTS idx_dim_emp_hire_date
    ON people_analytics.dim_employees (hire_date);

-- 3. dim_salary_benchmarks Indexes
CREATE INDEX IF NOT EXISTS idx_dim_bmk_current
    ON people_analytics.dim_salary_benchmarks (position_sk, country_code)
    WHERE is_current_benchmark = TRUE;

-- 4. fact_attendance_logs Indexes
CREATE INDEX IF NOT EXISTS idx_fact_att_date_sk
    ON people_analytics.fact_attendance_logs (date_sk);

CREATE INDEX IF NOT EXISTS idx_fact_att_bradford
    ON people_analytics.fact_attendance_logs (employee_sk, date_key)
    INCLUDE (is_absence_instance_start)
    WHERE is_unplanned_absence = TRUE;

CREATE INDEX IF NOT EXISTS idx_fact_att_overtime
    ON people_analytics.fact_attendance_logs (employee_sk, date_key)
    WHERE overtime_hours > 0;

-- 5. fact_terminations Indexes
CREATE INDEX IF NOT EXISTS idx_fact_trm_date_type
    ON people_analytics.fact_terminations (termination_date_sk, termination_type);

CREATE INDEX IF NOT EXISTS idx_fact_trm_regrettable
    ON people_analytics.fact_terminations (employee_sk)
    WHERE is_regrettable_attrition = TRUE;

-- 6. fact_sla_events Indexes
CREATE INDEX IF NOT EXISTS idx_fact_sla_dept_date
    ON people_analytics.fact_sla_events (department_sk, event_date_sk);

CREATE INDEX IF NOT EXISTS idx_fact_sla_staffing
    ON people_analytics.fact_sla_events (department_sk)
    WHERE attributed_to_staffing_deficit = TRUE;
