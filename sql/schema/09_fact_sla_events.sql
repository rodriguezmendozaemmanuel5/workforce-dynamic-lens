-- =============================================================================
-- WORKFORCE DYNAMIC LENS — MODULE v0.6.0
-- Script 09: Fact Table — fact_sla_events
-- Engine Target: PostgreSQL 15+
-- Design Freeze Baseline: v1.0 (August 2026)
-- Author: Emmanuel Rodríguez Mendoza
-- =============================================================================

SET search_path TO people_analytics, public;

CREATE TABLE IF NOT EXISTS people_analytics.fact_sla_events (
    sla_event_sk                    BIGINT GENERATED ALWAYS AS IDENTITY,
    sla_event_id                    VARCHAR(25) NOT NULL,
    department_sk                   BIGINT NOT NULL,
    event_date_sk                   INTEGER NOT NULL,
    event_date                      DATE NOT NULL,
    client_contract_id              VARCHAR(20) NOT NULL,
    shift_id                        VARCHAR(20) NOT NULL,
    breach_type                     VARCHAR(50) NOT NULL,
    hours_delayed                   NUMERIC(4,2) NOT NULL,
    penalty_cost_usd                NUMERIC(10,2) NOT NULL,
    attributed_to_staffing_deficit  BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT pk_fact_sla_events PRIMARY KEY (sla_event_sk),
    CONSTRAINT uq_fact_sla_id UNIQUE (sla_event_id),
    CONSTRAINT fk_fact_sla_dim_dept FOREIGN KEY (department_sk)
        REFERENCES people_analytics.dim_departments (department_sk)
        ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT fk_fact_sla_dim_date FOREIGN KEY (event_date_sk)
        REFERENCES people_analytics.dim_date (date_sk)
        ON DELETE RESTRICT ON UPDATE RESTRICT
);

COMMENT ON TABLE people_analytics.fact_sla_events IS 'Fact Table tracking B2B SLA breach penalties and attribution to staffing deficits';
COMMENT ON COLUMN people_analytics.fact_sla_events.attributed_to_staffing_deficit IS 'Flag indicating breach caused by unstaffed shifts (BR-14 / KPI-FIN-02)';
