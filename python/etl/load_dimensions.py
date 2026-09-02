# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.7.0
# ETL Layer: Dimension Loaders (Topological Order)
# =============================================================================

import pandas as pd
import numpy as np
from pathlib import Path
from sqlalchemy import text
from sqlalchemy.engine import Engine
from python.data_generation.utils.logger import setup_logger
from python.etl.logging import log_start, log_success, log_failure

logger = setup_logger("etl.load_dimensions")
DATASETS_PATH = Path("datasets/generated")


def load_dim_date(engine: Engine, start: str = "2012-01-01",
                  end: str = "2030-12-31") -> int:
    """
    Generates and inserts dim_date if the table is empty.
    Uses YYYYMMDD integer as the surrogate key (no IDENTITY).
    """
    with engine.connect() as conn:
        count = conn.execute(
            text("SELECT COUNT(*) FROM people_analytics.dim_date")
        ).scalar()
    if count > 0:
        logger.info(f"[dim_date] Already populated ({count} rows). Skipping.")
        return count

    date_range = pd.date_range(start=start, end=end, freq="D")
    df = pd.DataFrame({
        "date_sk":            date_range.strftime("%Y%m%d").astype(int),
        "date_actual":        date_range.date,
        "year_number":        date_range.year.astype("int16"),
        "quarter_number":     date_range.quarter.astype("int16"),
        "month_number":       date_range.month.astype("int16"),
        "month_name":         date_range.strftime("%B"),
        "week_number_iso":    date_range.isocalendar().week.astype("int16"),
        "day_of_week_number": (date_range.dayofweek.astype("int16") + 1),  # 1=Mon
        "day_name":           date_range.strftime("%A"),
        "is_weekend":         date_range.dayofweek >= 5,
        "is_holiday":         False,
        "fiscal_year":        date_range.year.astype("int16"),
        "fiscal_quarter":     date_range.quarter.astype("int16"),
        "year_month_label":   date_range.strftime("%Y-%m"),
    })

    load_id = log_start(engine, "dim_date", "generated_in_etl")
    try:
        df.to_sql("dim_date", engine, schema="people_analytics",
                  if_exists="append", index=False, method="multi", chunksize=1000)
        log_success(engine, load_id, rows_inserted=len(df))
        logger.info(f"[dim_date] Inserted {len(df)} rows.")
        return len(df)
    except Exception as e:
        log_failure(engine, load_id, str(e))
        raise


def load_departments(engine: Engine) -> int:
    csv_path = DATASETS_PATH / "dim_departments.csv"
    df = pd.read_csv(csv_path, encoding="utf-8")
    load_id = log_start(engine, "dim_departments", str(csv_path))
    inserted = 0
    updated = 0
    try:
        with engine.begin() as conn:
            for _, row in df.iterrows():
                res = conn.execute(text("""
                    INSERT INTO people_analytics.dim_departments
                        (department_id, department_name, cost_center_code,
                         vp_responsible, region, budget_annual_usd,
                         target_headcount, strategic_level)
                    VALUES
                        (:department_id, :department_name, :cost_center_code,
                         :vp_responsible, :region, :budget_annual_usd,
                         :target_headcount, :strategic_level)
                    ON CONFLICT (department_id) DO UPDATE SET
                        department_name   = EXCLUDED.department_name,
                        cost_center_code  = EXCLUDED.cost_center_code,
                        vp_responsible    = EXCLUDED.vp_responsible,
                        region            = EXCLUDED.region,
                        budget_annual_usd = EXCLUDED.budget_annual_usd,
                        target_headcount  = EXCLUDED.target_headcount,
                        strategic_level   = EXCLUDED.strategic_level
                    RETURNING (xmax = 0) AS is_insert
                """), row.to_dict())
                if res.scalar():
                    inserted += 1
                else:
                    updated += 1
        log_success(engine, load_id, rows_inserted=inserted, rows_updated=updated)
        logger.info(f"[dim_departments] Loaded {len(df)} departments (inserted={inserted}, updated={updated}).")
        return len(df)
    except Exception as e:
        log_failure(engine, load_id, str(e))
        raise


def load_positions(engine: Engine) -> int:
    csv_path = DATASETS_PATH / "dim_positions.csv"
    df = pd.read_csv(csv_path, encoding="utf-8")
    load_id = log_start(engine, "dim_positions", str(csv_path))
    inserted = 0
    updated = 0
    try:
        with engine.begin() as conn:
            for _, row in df.iterrows():
                res = conn.execute(text("""
                    INSERT INTO people_analytics.dim_positions
                        (position_id, job_title, job_family, job_grade,
                         career_level, is_critical_position,
                         is_remote_eligible, market_scarcity_index)
                    VALUES
                        (:position_id, :job_title, :job_family, :job_grade,
                         :career_level, :is_critical_position,
                         :is_remote_eligible, :market_scarcity_index)
                    ON CONFLICT (position_id) DO UPDATE SET
                        job_title              = EXCLUDED.job_title,
                        job_family             = EXCLUDED.job_family,
                        job_grade              = EXCLUDED.job_grade,
                        career_level           = EXCLUDED.career_level,
                        is_critical_position   = EXCLUDED.is_critical_position,
                        is_remote_eligible     = EXCLUDED.is_remote_eligible,
                        market_scarcity_index  = EXCLUDED.market_scarcity_index
                    RETURNING (xmax = 0) AS is_insert
                """), row.to_dict())
                if res.scalar():
                    inserted += 1
                else:
                    updated += 1
        log_success(engine, load_id, rows_inserted=inserted, rows_updated=updated)
        logger.info(f"[dim_positions] Loaded {len(df)} positions (inserted={inserted}, updated={updated}).")
        return len(df)
    except Exception as e:
        log_failure(engine, load_id, str(e))
        raise


def load_salary_benchmarks(engine: Engine, pos_nk_to_sk: dict) -> int:
    csv_path = DATASETS_PATH / "dim_salary_benchmarks.csv"
    df = pd.read_csv(csv_path, encoding="utf-8")
    df["position_sk"] = df["position_id"].map(pos_nk_to_sk)

    orphans = df[df["position_sk"].isna()]
    if not orphans.empty:
        logger.warning(f"[dim_salary_benchmarks] {len(orphans)} rows with unknown position_id — skipping.")
        df = df.dropna(subset=["position_sk"])
    df["position_sk"] = df["position_sk"].astype("int64")

    load_id = log_start(engine, "dim_salary_benchmarks", str(csv_path))
    inserted = 0
    updated = 0
    try:
        with engine.begin() as conn:
            for _, row in df.iterrows():
                row_dict = {
                    "benchmark_id": row["benchmark_id"],
                    "position_sk": int(row["position_sk"]),
                    "country_code": row["country_code"],
                    "market_min_salary_usd": float(row["market_min_salary_usd"]),
                    "market_midpoint_salary_usd": float(row["market_midpoint_salary_usd"]),
                    "market_max_salary_usd": float(row["market_max_salary_usd"]),
                    "survey_provider": row["survey_provider"],
                    "effective_year": int(row["effective_year"]),
                    "is_current_benchmark": bool(row["is_current_benchmark"]),
                }
                res = conn.execute(text("""
                    INSERT INTO people_analytics.dim_salary_benchmarks
                        (benchmark_id, position_sk, country_code,
                         market_min_salary_usd, market_midpoint_salary_usd,
                         market_max_salary_usd, survey_provider,
                         effective_year, is_current_benchmark)
                    VALUES
                        (:benchmark_id, :position_sk, :country_code,
                         :market_min_salary_usd, :market_midpoint_salary_usd,
                         :market_max_salary_usd, :survey_provider,
                         :effective_year, :is_current_benchmark)
                    ON CONFLICT (benchmark_id) DO UPDATE SET
                        position_sk                = EXCLUDED.position_sk,
                        country_code               = EXCLUDED.country_code,
                        market_min_salary_usd      = EXCLUDED.market_min_salary_usd,
                        market_midpoint_salary_usd = EXCLUDED.market_midpoint_salary_usd,
                        market_max_salary_usd      = EXCLUDED.market_max_salary_usd,
                        survey_provider            = EXCLUDED.survey_provider,
                        effective_year             = EXCLUDED.effective_year,
                        is_current_benchmark       = EXCLUDED.is_current_benchmark
                    RETURNING (xmax = 0) AS is_insert
                """), row_dict)
                if res.scalar():
                    inserted += 1
                else:
                    updated += 1
        log_success(engine, load_id, rows_inserted=inserted, rows_updated=updated, rows_rejected=len(orphans))
        logger.info(f"[dim_salary_benchmarks] Loaded {len(df)} benchmarks (inserted={inserted}, updated={updated}).")
        return len(df)
    except Exception as e:
        log_failure(engine, load_id, str(e))
        raise


def load_employees(engine: Engine, dept_nk_to_sk: dict,
                   pos_nk_to_sk: dict) -> int:
    csv_path = DATASETS_PATH / "dim_employees.csv"
    df = pd.read_csv(csv_path, encoding="utf-8", low_memory=False)
    df["department_sk"] = df["department_id"].map(dept_nk_to_sk)
    df["position_sk"]   = df["position_id"].map(pos_nk_to_sk)

    orphans = df[df["department_sk"].isna() | df["position_sk"].isna()]
    if not orphans.empty:
        logger.warning(f"[dim_employees] {len(orphans)} orphan rows — skipping.")
        df = df.dropna(subset=["department_sk", "position_sk"])

    df["department_sk"] = df["department_sk"].astype("int64")
    df["position_sk"]   = df["position_sk"].astype("int64")

    db_cols = ["employee_id", "first_name", "last_name", "work_email",
               "gender", "birth_date", "hire_date", "department_sk",
               "position_sk", "country_code", "work_location_type",
               "base_salary_orig", "salary_currency_orig",
               "annual_base_salary_usd", "fully_loaded_cost_usd",
               "performance_rating", "potential_rating", "is_active",
               "is_current_row", "row_effective_date", "row_expiration_date"]

    load_id = log_start(engine, "dim_employees", str(csv_path))
    try:
        # Check existing SCD2 versions by composite identity (employee_id, row_effective_date)
        with engine.connect() as conn:
            existing_rows = conn.execute(text("""
                SELECT employee_id, row_effective_date::TEXT AS eff_date
                FROM people_analytics.dim_employees
            """)).fetchall()
            existing_keys = {(r.employee_id, r.eff_date) for r in existing_rows}

        df["eff_date_str"] = df["row_effective_date"].astype(str)
        is_new_mask = ~df.apply(lambda r: (r["employee_id"], r["eff_date_str"]) in existing_keys, axis=1)
        df_new = df[is_new_mask].drop(columns=["eff_date_str"])
        existing_count = len(df) - len(df_new)

        if not df_new.empty:
            df_new_sorted = df_new.sort_values(by="row_effective_date", ascending=True)
            with engine.begin() as conn:
                for _, row in df_new_sorted.iterrows():
                    if row["is_current_row"]:
                        conn.execute(text("""
                            UPDATE people_analytics.dim_employees
                            SET is_current_row = FALSE,
                                row_expiration_date = :eff_date
                            WHERE employee_id = :emp_id
                              AND is_current_row = TRUE
                        """), {
                            "emp_id": row["employee_id"],
                            "eff_date": row["row_effective_date"]
                        })
                df_new_sorted[db_cols].to_sql(
                    "dim_employees", conn, schema="people_analytics",
                    if_exists="append", index=False,
                    method="multi", chunksize=500
                )

        log_success(engine, load_id, rows_inserted=len(df_new),
                    rows_updated=existing_count, rows_rejected=len(orphans))
        logger.info(
            f"[dim_employees] Loaded {len(df)} rows "
            f"(inserted={len(df_new)}, existing_preserved={existing_count})."
        )
        return len(df)
    except Exception as e:
        log_failure(engine, load_id, str(e))
        raise
