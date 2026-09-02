-- =============================================================================
-- WORKFORCE DYNAMIC LENS — MODULE v0.6.0
-- Script 06: Dimension Table — dim_employees (SCD Type 2)
-- Engine Target: PostgreSQL 15+
-- Design Freeze Baseline: v1.0 (August 2026)
-- Author: Emmanuel Rodríguez Mendoza
-- =============================================================================

SET search_path TO people_analytics, public;

CREATE TABLE IF NOT EXISTS people_analytics.dim_employees (
    employee_sk             BIGINT GENERATED ALWAYS AS IDENTITY,
    employee_id             VARCHAR(10) NOT NULL,
    first_name              VARCHAR(50) NOT NULL,
    last_name               VARCHAR(50) NOT NULL,
    work_email              VARCHAR(100) NOT NULL,
    gender                  VARCHAR(20) NOT NULL,
    birth_date              DATE NOT NULL,
    hire_date               DATE NOT NULL,
    department_sk           BIGINT NOT NULL,
    position_sk             BIGINT NOT NULL,
    country_code            VARCHAR(3) NOT NULL,
    work_location_type      VARCHAR(20) NOT NULL,
    base_salary_orig        NUMERIC(12,2) NOT NULL,
    salary_currency_orig    VARCHAR(3) NOT NULL,
    annual_base_salary_usd  NUMERIC(12,2) NOT NULL,
    fully_loaded_cost_usd   NUMERIC(12,2) NOT NULL,
    performance_rating      NUMERIC(3,2) NULL,
    potential_rating        VARCHAR(10) NULL,
    is_active               BOOLEAN NOT NULL DEFAULT TRUE,
    is_current_row          BOOLEAN NOT NULL DEFAULT TRUE,
    row_effective_date      DATE NOT NULL DEFAULT CURRENT_DATE,
    row_expiration_date     DATE NOT NULL DEFAULT '9999-12-31',

    CONSTRAINT pk_dim_employees PRIMARY KEY (employee_sk),
    CONSTRAINT fk_dim_emp_dim_dept FOREIGN KEY (department_sk)
        REFERENCES people_analytics.dim_departments (department_sk)
        ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT fk_dim_emp_dim_pos FOREIGN KEY (position_sk)
        REFERENCES people_analytics.dim_positions (position_sk)
        ON DELETE RESTRICT ON UPDATE RESTRICT
);

COMMENT ON TABLE people_analytics.dim_employees IS 'Central Employee Dimension implementing SCD Type 2 for historical tracking';
COMMENT ON COLUMN people_analytics.dim_employees.employee_sk IS 'Surrogate Primary Key (Identity)';
COMMENT ON COLUMN people_analytics.dim_employees.employee_id IS 'Natural Business Key (e.g., EMP01420)';
COMMENT ON COLUMN people_analytics.dim_employees.is_current_row IS 'SCD2 flag — TRUE for active historical version';
COMMENT ON COLUMN people_analytics.dim_employees.row_expiration_date IS 'SCD2 sentinel date — 9999-12-31 for current records';
