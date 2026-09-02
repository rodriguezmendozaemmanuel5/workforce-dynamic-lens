# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.7.0
# ETL Layer: Fact Table Loaders
# =============================================================================

import pandas as pd
import numpy as np
from pathlib import Path
from sqlalchemy import MetaData
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.engine import Engine
from python.data_generation.utils.logger import setup_logger
from python.etl.logging import log_start, log_success, log_failure

logger = setup_logger("etl.load_facts")
DATASETS_PATH = Path("datasets/generated")
CHUNK_SIZE = 10_000


def _map_and_validate(df: pd.DataFrame, col: str, lookup: dict,
                      table: str) -> pd.DataFrame:
    """Maps NK column to SK via lookup; sends unresolved rows to warning log."""
    df[col] = df[col].map(lookup)
    orphans = df[df[col].isna()]
    if not orphans.empty:
        logger.warning(f"[{table}] {len(orphans)} rows with unresolvable {col} — dropping.")
        df = df.dropna(subset=[col])
    df[col] = df[col].astype("int64")
    return df


def load_attendance(engine: Engine, emp_nk_to_sk: dict,
                    date_lookup: dict) -> int:
    """
    Loads fact_attendance_logs in chunks of 10,000 rows.
    ~1.5M rows — chunked streaming avoids memory exhaustion, and
    ON CONFLICT (attendance_id) DO NOTHING guarantees idempotency.
    """
    csv_path = DATASETS_PATH / "fact_attendance_logs.csv"
    load_id = log_start(engine, "fact_attendance_logs", str(csv_path))
    total_inserted = 0
    total_rejected = 0

    metadata = MetaData()
    metadata.reflect(bind=engine, schema="people_analytics", only=["fact_attendance_logs"])
    att_table = metadata.tables["people_analytics.fact_attendance_logs"]

    db_cols = ["attendance_id", "employee_sk", "date_sk", "date_key",
               "shift_type", "clock_in_time", "clock_out_time",
               "planned_hours", "actual_hours_worked", "overtime_hours",
               "absence_type", "is_unplanned_absence", "is_absence_instance_start"]

    try:
        with engine.begin() as conn:
            for chunk_num, chunk in enumerate(
                pd.read_csv(csv_path, chunksize=CHUNK_SIZE, encoding="utf-8", low_memory=False), start=1
            ):
                before = len(chunk)
                chunk["employee_sk"] = chunk["employee_id"].map(emp_nk_to_sk)
                chunk["date_sk"] = chunk["date_key"].map(date_lookup)

                chunk = chunk.dropna(subset=["employee_sk", "date_sk"])
                chunk["employee_sk"] = chunk["employee_sk"].astype("int64")
                chunk["date_sk"] = chunk["date_sk"].astype("int32")

                rejected = before - len(chunk)
                total_rejected += rejected

                cols_present = [c for c in db_cols if c in chunk.columns]
                chunk_data = chunk[cols_present]

                # Convert NaNs to None so PostgreSQL treats them as proper SQL NULLs
                records = [
                    {k: (None if pd.isna(v) else v) for k, v in row.items()}
                    for row in chunk_data.to_dict(orient="records")
                ]

                if records:
                    stmt = (
                        pg_insert(att_table)
                        .values(records)
                        .on_conflict_do_nothing(index_elements=["attendance_id"])
                    )
                    res = conn.execute(stmt)
                    total_inserted += res.rowcount

                if chunk_num % 50 == 0:
                    logger.info(f"[fact_attendance_logs] Chunk {chunk_num} processed — {total_inserted:,} rows inserted so far.")

        log_success(engine, load_id, rows_inserted=total_inserted,
                    rows_rejected=total_rejected)
        logger.info(f"[fact_attendance_logs] Load complete — {total_inserted:,} rows inserted, {total_rejected} rejected.")
        return total_inserted

    except Exception as e:
        log_failure(engine, load_id, str(e))
        raise


def load_terminations(engine: Engine, emp_nk_to_sk: dict,
                      date_lookup: dict) -> int:
    csv_path = DATASETS_PATH / "fact_terminations.csv"
    df = pd.read_csv(csv_path, encoding="utf-8")
    load_id = log_start(engine, "fact_terminations", str(csv_path))

    metadata = MetaData()
    metadata.reflect(bind=engine, schema="people_analytics", only=["fact_terminations"])
    trm_table = metadata.tables["people_analytics.fact_terminations"]

    df["employee_sk"]        = df["employee_id"].map(emp_nk_to_sk)
    df["termination_date_sk"] = df["termination_date"].map(date_lookup)
    before = len(df)
    df = df.dropna(subset=["employee_sk", "termination_date_sk"])
    rejected = before - len(df)

    df["employee_sk"]        = df["employee_sk"].astype("int64")
    df["termination_date_sk"] = df["termination_date_sk"].astype("int32")

    db_cols = ["termination_id", "employee_sk", "termination_date_sk",
               "termination_date", "termination_type", "hris_exit_reason",
               "proxy_reclassified_reason", "severance_cost_usd",
               "notice_period_days", "is_regrettable_attrition"]

    cols_present = [c for c in db_cols if c in df.columns]
    records = [
        {k: (None if pd.isna(v) else v) for k, v in row.items()}
        for row in df[cols_present].to_dict(orient="records")
    ]

    try:
        with engine.begin() as conn:
            stmt = (
                pg_insert(trm_table)
                .values(records)
                .on_conflict_do_nothing(index_elements=["termination_id"])
            )
            res = conn.execute(stmt)
            inserted = res.rowcount

        log_success(engine, load_id, rows_inserted=inserted,
                    rows_rejected=rejected)
        logger.info(f"[fact_terminations] Loaded {len(df)} rows (inserted={inserted}, rejected={rejected}).")
        return inserted
    except Exception as e:
        log_failure(engine, load_id, str(e))
        raise


def load_sla_events(engine: Engine, dept_nk_to_sk: dict,
                    date_lookup: dict) -> int:
    csv_path = DATASETS_PATH / "fact_sla_events.csv"
    df = pd.read_csv(csv_path, encoding="utf-8")
    load_id = log_start(engine, "fact_sla_events", str(csv_path))

    metadata = MetaData()
    metadata.reflect(bind=engine, schema="people_analytics", only=["fact_sla_events"])
    sla_table = metadata.tables["people_analytics.fact_sla_events"]

    df["department_sk"]  = df["department_id"].map(dept_nk_to_sk)
    df["event_date_sk"]  = df["event_date"].map(date_lookup)
    before = len(df)
    df = df.dropna(subset=["department_sk", "event_date_sk"])
    rejected = before - len(df)

    df["department_sk"]  = df["department_sk"].astype("int64")
    df["event_date_sk"]  = df["event_date_sk"].astype("int32")

    db_cols = ["sla_event_id", "department_sk", "event_date_sk",
               "event_date", "client_contract_id", "shift_id",
               "breach_type", "hours_delayed", "penalty_cost_usd",
               "attributed_to_staffing_deficit"]

    cols_present = [c for c in db_cols if c in df.columns]
    records = [
        {k: (None if pd.isna(v) else v) for k, v in row.items()}
        for row in df[cols_present].to_dict(orient="records")
    ]

    try:
        with engine.begin() as conn:
            stmt = (
                pg_insert(sla_table)
                .values(records)
                .on_conflict_do_nothing(index_elements=["sla_event_id"])
            )
            res = conn.execute(stmt)
            inserted = res.rowcount

        log_success(engine, load_id, rows_inserted=inserted,
                    rows_rejected=rejected)
        logger.info(f"[fact_sla_events] Loaded {len(df)} rows (inserted={inserted}, rejected={rejected}).")
        return inserted
    except Exception as e:
        log_failure(engine, load_id, str(e))
        raise
