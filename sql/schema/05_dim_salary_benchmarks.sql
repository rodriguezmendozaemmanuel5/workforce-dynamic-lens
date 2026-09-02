-- =============================================================================
-- WORKFORCE DYNAMIC LENS — MODULE v0.6.0
-- Script 05: Dimension Table — dim_salary_benchmarks
-- Engine Target: PostgreSQL 15+
-- Design Freeze Baseline: v1.0 (August 2026)
-- Author: Emmanuel Rodríguez Mendoza
-- =============================================================================

SET search_path TO people_analytics, public;

CREATE TABLE IF NOT EXISTS people_analytics.dim_salary_benchmarks (
    benchmark_sk                BIGINT GENERATED ALWAYS AS IDENTITY,
    benchmark_id                VARCHAR(25) NOT NULL,
    position_sk                 BIGINT NOT NULL,
    country_code                VARCHAR(3) NOT NULL,
    market_min_salary_usd       NUMERIC(12,2) NOT NULL,
    market_midpoint_salary_usd  NUMERIC(12,2) NOT NULL,
    market_max_salary_usd       NUMERIC(12,2) NOT NULL,
    survey_provider             VARCHAR(50) NOT NULL,
    effective_year              SMALLINT NOT NULL,
    is_current_benchmark        BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT pk_dim_salary_benchmarks PRIMARY KEY (benchmark_sk),
    CONSTRAINT uq_dim_bmk_id UNIQUE (benchmark_id),
    CONSTRAINT fk_dim_bmk_dim_pos FOREIGN KEY (position_sk)
        REFERENCES people_analytics.dim_positions (position_sk)
        ON DELETE RESTRICT ON UPDATE RESTRICT
);

COMMENT ON TABLE people_analytics.dim_salary_benchmarks IS 'Market Salary Benchmarks by position and country for Compa-Ratio calculations';
COMMENT ON COLUMN people_analytics.dim_salary_benchmarks.is_current_benchmark IS 'Flag indicating active benchmark for Compa-Ratio joins (AUD-11)';
