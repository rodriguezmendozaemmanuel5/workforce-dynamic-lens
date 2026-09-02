-- =============================================================================
-- WORKFORCE DYNAMIC LENS — MODULE v0.6.0
-- Script 11: Named CHECK Constraints Enforcement
-- Engine Target: PostgreSQL 15+
-- Design Freeze Baseline: v1.0 (August 2026)
-- Author: Emmanuel Rodríguez Mendoza
-- =============================================================================

SET search_path TO people_analytics, public;

-- 1. dim_date
ALTER TABLE people_analytics.dim_date
    ADD CONSTRAINT chk_date_sk_format CHECK (date_sk BETWEEN 20100101 AND 20991231),
    ADD CONSTRAINT chk_date_quarter CHECK (quarter_number BETWEEN 1 AND 4),
    ADD CONSTRAINT chk_date_month CHECK (month_number BETWEEN 1 AND 12),
    ADD CONSTRAINT chk_date_dow CHECK (day_of_week_number BETWEEN 1 AND 7);

-- 2. dim_departments
ALTER TABLE people_analytics.dim_departments
    ADD CONSTRAINT chk_dept_id_format CHECK (department_id ~ '^DEP_[A-Z0-9_]+$'),
    ADD CONSTRAINT chk_dept_budget_positive CHECK (budget_annual_usd > 0),
    ADD CONSTRAINT chk_dept_headcount_positive CHECK (target_headcount > 0),
    ADD CONSTRAINT chk_dept_strategic_level CHECK (strategic_level IN ('Core Revenue', 'Operation Critical', 'Support')),
    ADD CONSTRAINT chk_dept_region CHECK (region IN ('LATAM', 'Europa', 'Global'));

-- 3. dim_positions
ALTER TABLE people_analytics.dim_positions
    ADD CONSTRAINT chk_pos_id_format CHECK (position_id ~ '^POS_[A-Z0-9_]+$'),
    ADD CONSTRAINT chk_pos_scarcity_range CHECK (market_scarcity_index BETWEEN 1.00 AND 3.00),
    ADD CONSTRAINT chk_pos_career_level CHECK (career_level IN ('Junior', 'SemiSenior', 'Senior', 'Lead', 'Director', 'Executive'));

-- 4. dim_salary_benchmarks
ALTER TABLE people_analytics.dim_salary_benchmarks
    ADD CONSTRAINT chk_bmk_id_format CHECK (benchmark_id ~ '^BMK_[A-Z0-9_]+$'),
    ADD CONSTRAINT chk_bmk_ordering CHECK (market_min_salary_usd < market_midpoint_salary_usd AND market_midpoint_salary_usd < market_max_salary_usd),
    ADD CONSTRAINT chk_bmk_effective_year CHECK (effective_year BETWEEN 2020 AND 2035),
    ADD CONSTRAINT chk_bmk_country_code CHECK (country_code IN ('MEX','COL','BRA','CHL','ARG','ESP','DEU','USA','GBR'));

-- 5. dim_employees
ALTER TABLE people_analytics.dim_employees
    ADD CONSTRAINT chk_emp_id_format CHECK (employee_id ~ '^EMP[0-9]{5}$'),
    ADD CONSTRAINT chk_emp_salary_range CHECK (annual_base_salary_usd > 0 AND annual_base_salary_usd <= 300000),
    ADD CONSTRAINT chk_emp_fully_loaded CHECK (fully_loaded_cost_usd > 0),
    ADD CONSTRAINT chk_emp_base_salary CHECK (base_salary_orig > 0),
    ADD CONSTRAINT chk_emp_perf_range CHECK (performance_rating IS NULL OR (performance_rating BETWEEN 1.00 AND 5.00)),
    ADD CONSTRAINT chk_emp_potential CHECK (potential_rating IS NULL OR potential_rating IN ('Bajo', 'Medio', 'Alto', 'Top Talent')),
    ADD CONSTRAINT chk_emp_gender CHECK (gender IN ('Masculino', 'Femenino', 'No Binario', 'Prefiero no decirlo')),
    ADD CONSTRAINT chk_emp_work_location CHECK (work_location_type IN ('Presencial', 'Híbrido', 'Remoto')),
    ADD CONSTRAINT chk_emp_country_code CHECK (country_code IN ('MEX','COL','BRA','CHL','ARG','ESP','DEU','USA','GBR')),
    ADD CONSTRAINT chk_emp_currency CHECK (salary_currency_orig IN ('MXN','COP','BRL','CLP','ARS','EUR','USD','GBP')),
    ADD CONSTRAINT chk_emp_scd2_dates CHECK (row_expiration_date >= row_effective_date),
    ADD CONSTRAINT chk_emp_hire_date_min CHECK (hire_date >= '2010-01-01'),
    ADD CONSTRAINT chk_emp_work_email CHECK (work_email LIKE '%@%');

-- 6. fact_attendance_logs
ALTER TABLE people_analytics.fact_attendance_logs
    ADD CONSTRAINT chk_att_id_format CHECK (attendance_id ~ '^ATT_[0-9]{12,16}$'),
    ADD CONSTRAINT chk_att_planned_hours CHECK (planned_hours BETWEEN 0.00 AND 12.00),
    ADD CONSTRAINT chk_att_actual_hours CHECK (actual_hours_worked BETWEEN 0.00 AND 16.00),
    ADD CONSTRAINT chk_att_overtime_positive CHECK (overtime_hours >= 0.00),
    ADD CONSTRAINT chk_att_clock_order CHECK (clock_in_time IS NULL OR clock_out_time IS NULL OR (clock_out_time > clock_in_time AND clock_out_time - clock_in_time < INTERVAL '24 hours')),
    ADD CONSTRAINT chk_att_shift_type CHECK (shift_type IN ('Mañana', 'Tarde', 'Noche', 'Central')),
    ADD CONSTRAINT chk_att_absence_type CHECK (absence_type IS NULL OR absence_type IN ('Incapacidad Medica', 'Vacaciones', 'Injustificada', 'Licencia Legal', 'Permiso Autorizado')),
    ADD CONSTRAINT chk_att_absence_consistency CHECK (NOT (is_unplanned_absence = TRUE AND absence_type IN ('Vacaciones', 'Licencia Legal', 'Permiso Autorizado')));

-- 7. fact_terminations
ALTER TABLE people_analytics.fact_terminations
    ADD CONSTRAINT chk_trm_id_format CHECK (termination_id ~ '^TRM_[0-9]{8,14}$'),
    ADD CONSTRAINT chk_trm_type CHECK (termination_type IN ('Voluntaria', 'Involuntaria', 'Jubilacion', 'Mutual Acuerdo', 'Fallecimiento')),
    ADD CONSTRAINT chk_trm_severance_nonneg CHECK (severance_cost_usd >= 0.00),
    ADD CONSTRAINT chk_trm_notice_period CHECK (notice_period_days BETWEEN 0 AND 90),
    ADD CONSTRAINT chk_trm_date_min CHECK (termination_date >= '2010-01-01');

-- 8. fact_sla_events
ALTER TABLE people_analytics.fact_sla_events
    ADD CONSTRAINT chk_sla_id_format CHECK (sla_event_id ~ '^SLA_[0-9]{8,14}$'),
    ADD CONSTRAINT chk_sla_hours_delayed CHECK (hours_delayed > 0.00),
    ADD CONSTRAINT chk_sla_penalty_positive CHECK (penalty_cost_usd > 0.00),
    ADD CONSTRAINT chk_sla_shift_id CHECK (shift_id IN ('Mañana', 'Tarde', 'Noche')),
    ADD CONSTRAINT chk_sla_event_date_min CHECK (event_date >= '2020-01-01');
