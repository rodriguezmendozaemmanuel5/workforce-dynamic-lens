-- =============================================================================
-- WORKFORCE DYNAMIC LENS — MODULE v0.6.0
-- Script 10: Staging & Operational Support Tables
-- Engine Target: PostgreSQL 15+
-- Design Freeze Baseline: v1.0 (August 2026)
-- Author: Emmanuel Rodríguez Mendoza
-- =============================================================================

SET search_path TO people_analytics, public;

-- 1. Data Quality Quarantine Table
CREATE TABLE IF NOT EXISTS people_analytics.stg_quarantine_records (
    quarantine_id       BIGINT GENERATED ALWAYS AS IDENTITY,
    source_table        VARCHAR(50) NOT NULL,
    source_pk_value     VARCHAR(50) NOT NULL,
    dq_rule_id          VARCHAR(20) NOT NULL,
    severity_level      VARCHAR(10) NOT NULL,
    error_message       TEXT NOT NULL,
    raw_record_json     JSONB NULL,
    quarantine_date     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolved            BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT pk_stg_quarantine PRIMARY KEY (quarantine_id)
);

COMMENT ON TABLE people_analytics.stg_quarantine_records IS 'Quarantine table for records failing Data Contract validation rules';

-- 2. Machine Learning Model Predictions Placeholder (v0.7.0)
CREATE TABLE IF NOT EXISTS people_analytics.stg_model_predictions (
    prediction_id       BIGINT GENERATED ALWAYS AS IDENTITY,
    employee_sk         BIGINT NOT NULL,
    flight_risk_score   NUMERIC(4,3) NOT NULL,
    risk_tier           VARCHAR(10) NOT NULL,
    inference_date      DATE NOT NULL DEFAULT CURRENT_DATE,
    model_version       VARCHAR(20) NOT NULL DEFAULT 'v0.7.0',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT pk_stg_model_predictions PRIMARY KEY (prediction_id),
    CONSTRAINT fk_stg_pred_dim_emp FOREIGN KEY (employee_sk)
        REFERENCES people_analytics.dim_employees (employee_sk)
        ON DELETE RESTRICT ON UPDATE RESTRICT
);

COMMENT ON TABLE people_analytics.stg_model_predictions IS 'Placeholder table for XGBoost Flight Risk predictions (v0.7.0 ML Pipeline)';

-- 3. ETL Operations & Audit History Table
CREATE TABLE IF NOT EXISTS people_analytics.etl_load_history (
    load_id             BIGINT GENERATED ALWAYS AS IDENTITY,
    load_start_ts       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    load_end_ts         TIMESTAMPTZ NULL,
    target_table        VARCHAR(50) NOT NULL,
    source_system       VARCHAR(50) NOT NULL DEFAULT 'synthetic_generator',
    rows_inserted       INTEGER NOT NULL DEFAULT 0,
    rows_updated        INTEGER NOT NULL DEFAULT 0,
    rows_rejected       INTEGER NOT NULL DEFAULT 0,
    status              VARCHAR(10) NOT NULL,
    source_file         VARCHAR(255) NULL,
    checksum            VARCHAR(64) NULL,
    error_message       TEXT NULL,

    CONSTRAINT pk_etl_load_history PRIMARY KEY (load_id)
);

COMMENT ON TABLE people_analytics.etl_load_history IS 'Operational logging and audit history table for ETL pipeline runs';
