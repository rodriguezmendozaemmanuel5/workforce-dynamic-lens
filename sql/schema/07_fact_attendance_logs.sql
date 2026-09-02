-- =============================================================================
-- WORKFORCE DYNAMIC LENS — MODULE v0.6.0
-- Script 07: Fact Table — fact_attendance_logs
-- Engine Target: PostgreSQL 15+
-- Design Freeze Baseline: v1.0 (August 2026)
-- Author: Emmanuel Rodríguez Mendoza
-- =============================================================================

SET search_path TO people_analytics, public;

CREATE TABLE IF NOT EXISTS people_analytics.fact_attendance_logs (
    attendance_sk               BIGINT GENERATED ALWAYS AS IDENTITY,
    attendance_id               VARCHAR(25) NOT NULL,
    employee_sk                 BIGINT NOT NULL,
    date_sk                     INTEGER NOT NULL,
    date_key                    DATE NOT NULL,
    shift_type                  VARCHAR(20) NOT NULL,
    clock_in_time               TIMESTAMPTZ NULL,
    clock_out_time              TIMESTAMPTZ NULL,
    planned_hours               NUMERIC(4,2) NOT NULL,
    actual_hours_worked         NUMERIC(4,2) NOT NULL,
    overtime_hours              NUMERIC(4,2) NOT NULL DEFAULT 0.00,
    absence_type                VARCHAR(30) NULL,
    is_unplanned_absence        BOOLEAN NOT NULL DEFAULT FALSE,
    is_absence_instance_start   BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT pk_fact_attendance_logs PRIMARY KEY (attendance_sk),
    CONSTRAINT uq_fact_att_id UNIQUE (attendance_id),
    CONSTRAINT uq_fact_att_emp_date UNIQUE (employee_sk, date_key),
    CONSTRAINT fk_fact_att_dim_emp FOREIGN KEY (employee_sk)
        REFERENCES people_analytics.dim_employees (employee_sk)
        ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT fk_fact_att_dim_date FOREIGN KEY (date_sk)
        REFERENCES people_analytics.dim_date (date_sk)
        ON DELETE RESTRICT ON UPDATE RESTRICT
);

COMMENT ON TABLE people_analytics.fact_attendance_logs IS 'Fact Table recording daily attendance, clock times, absences, and Bradford factor flags';
COMMENT ON COLUMN people_analytics.fact_attendance_logs.date_sk IS 'FK to dim_date (YYYYMMDD) for Power BI DAX Time Intelligence';
COMMENT ON COLUMN people_analytics.fact_attendance_logs.date_key IS 'Redundant DATE column for direct SQL filter optimization (OBS-01)';
COMMENT ON COLUMN people_analytics.fact_attendance_logs.clock_in_time IS 'TIMESTAMPTZ stored in UTC';
