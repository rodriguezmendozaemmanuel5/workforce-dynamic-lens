-- =============================================================================
-- WORKFORCE DYNAMIC LENS — MODULE v0.6.0
-- Script 02: Dimension Table — dim_date
-- Engine Target: PostgreSQL 15+
-- Design Freeze Baseline: v1.0 (August 2026)
-- Author: Emmanuel Rodríguez Mendoza
-- =============================================================================

SET search_path TO people_analytics, public;

CREATE TABLE IF NOT EXISTS people_analytics.dim_date (
    date_sk             INTEGER NOT NULL,
    date_actual         DATE NOT NULL,
    year_number         SMALLINT NOT NULL,
    quarter_number      SMALLINT NOT NULL,
    month_number        SMALLINT NOT NULL,
    month_name          VARCHAR(12) NOT NULL,
    week_number_iso     SMALLINT NOT NULL,
    day_of_week_number  SMALLINT NOT NULL,
    day_name            VARCHAR(12) NOT NULL,
    is_weekend          BOOLEAN NOT NULL,
    is_holiday          BOOLEAN NOT NULL DEFAULT FALSE,
    fiscal_year         SMALLINT NOT NULL,
    fiscal_quarter      SMALLINT NOT NULL,
    year_month_label    VARCHAR(7) NOT NULL,

    CONSTRAINT pk_dim_date PRIMARY KEY (date_sk),
    CONSTRAINT uq_dim_date_actual UNIQUE (date_actual)
);

COMMENT ON TABLE people_analytics.dim_date IS 'Kimball Date Dimension for Time Intelligence analytics in Power BI';
COMMENT ON COLUMN people_analytics.dim_date.date_sk IS 'Surrogate Key in YYYYMMDD integer format (e.g., 20260804)';
COMMENT ON COLUMN people_analytics.dim_date.date_actual IS 'Actual calendar date for direct SQL join and Power BI Date Table marking';
