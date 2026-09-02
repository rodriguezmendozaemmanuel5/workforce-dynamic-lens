-- =============================================================================
-- WORKFORCE DYNAMIC LENS — MODULE v0.6.0
-- Script 08: Fact Table — fact_terminations
-- Engine Target: PostgreSQL 15+
-- Design Freeze Baseline: v1.0 (August 2026)
-- Author: Emmanuel Rodríguez Mendoza
-- =============================================================================

SET search_path TO people_analytics, public;

CREATE TABLE IF NOT EXISTS people_analytics.fact_terminations (
    termination_sk              BIGINT GENERATED ALWAYS AS IDENTITY,
    termination_id              VARCHAR(25) NOT NULL,
    employee_sk                 BIGINT NOT NULL,
    termination_date_sk         INTEGER NOT NULL,
    termination_date            DATE NOT NULL,
    termination_type            VARCHAR(20) NOT NULL,
    hris_exit_reason            VARCHAR(100) NOT NULL,
    proxy_reclassified_reason   VARCHAR(100) NOT NULL,
    severance_cost_usd          NUMERIC(12,2) NOT NULL DEFAULT 0.00,
    notice_period_days          SMALLINT NOT NULL DEFAULT 0,
    is_regrettable_attrition    BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT pk_fact_terminations PRIMARY KEY (termination_sk),
    CONSTRAINT uq_fact_trm_id UNIQUE (termination_id),
    CONSTRAINT uq_fact_trm_emp_date UNIQUE (employee_sk, termination_date),
    CONSTRAINT fk_fact_trm_dim_emp FOREIGN KEY (employee_sk)
        REFERENCES people_analytics.dim_employees (employee_sk)
        ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT fk_fact_trm_dim_date FOREIGN KEY (termination_date_sk)
        REFERENCES people_analytics.dim_date (date_sk)
        ON DELETE RESTRICT ON UPDATE RESTRICT
);

COMMENT ON TABLE people_analytics.fact_terminations IS 'Fact Table storing employee offboarding events, exit reason proxies, and financial severance impact';
COMMENT ON COLUMN people_analytics.fact_terminations.proxy_reclassified_reason IS 'Reclassified exit reason resolving survey bias (BR-23 / FR-09)';
COMMENT ON COLUMN people_analytics.fact_terminations.termination_date_sk IS 'FK to dim_date for Time Intelligence DAX';
