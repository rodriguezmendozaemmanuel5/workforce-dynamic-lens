# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.7.0
# Main Orchestration Pipeline: Synthetic Data Generation & Export
# =============================================================================

import os
import json
import pandas as pd
from pathlib import Path

from python.data_generation.utils.config_loader import ConfigLoader
from python.data_generation.utils.random_state import SeedManager
from python.data_generation.utils.logger import setup_logger

from python.data_generation.generators.department_generator import generate_departments
from python.data_generation.generators.position_generator import generate_positions
from python.data_generation.generators.salary_benchmark_generator import generate_salary_benchmarks
from python.data_generation.generators.employee_generator import generate_employees
from python.data_generation.generators.attendance_generator import generate_attendance_logs
from python.data_generation.generators.termination_generator import generate_terminations
from python.data_generation.generators.sla_generator import generate_sla_events

from python.data_generation.validators.dataset_validator import DatasetValidator

logger = setup_logger("generate_dataset")

def generate_dim_date_df(start: str = "2012-01-01", end: str = "2030-12-31") -> pd.DataFrame:
    """Generates a complete static dim_date DataFrame for CSV export."""
    date_range = pd.date_range(start=start, end=end, freq="D")
    df = pd.DataFrame({
        "date_sk":            date_range.strftime("%Y%m%d").astype(int),
        "date_actual":        date_range.strftime("%Y-%m-%d"),
        "year_number":        date_range.year.astype("int16"),
        "quarter_number":     date_range.quarter.astype("int16"),
        "month_number":       date_range.month.astype("int16"),
        "month_name":         date_range.strftime("%B"),
        "week_number_iso":    date_range.isocalendar().week.astype("int16"),
        "day_of_week_number": (date_range.dayofweek.astype("int16") + 1),
        "day_name":           date_range.strftime("%A"),
        "is_weekend":         date_range.dayofweek >= 5,
        "is_holiday":         False,
        "fiscal_year":        date_range.year.astype("int16"),
        "fiscal_quarter":     date_range.quarter.astype("int16"),
        "year_month_label":   date_range.strftime("%Y-%m"),
    })
    return df

def run_generation_pipeline(output_dir: str = "datasets/generated"):
    """
    Executes end-to-end generation sequence in topological order:
    Dimensions -> Employees -> Terminations -> Reconcile State -> Attendance -> SLA -> Validation -> Export
    """
    logger.info("============================================================")
    logger.info("WORKFORCE DYNAMIC LENS — SYNTHETIC DATA GENERATOR v0.7.0")
    logger.info("============================================================")

    # Initialize fixed seed (seed=42)
    SeedManager.set_seed(42)
    config_loader = ConfigLoader()

    # 1. Generate Static Date Dimension
    logger.info("Generating Dimension 0: dim_date...")
    date_df = generate_dim_date_df()

    # 2. Generate Dimension DataFrames (Topological Order)
    logger.info("Generating Dimension 1: dim_departments...")
    depts_df = generate_departments(config_loader)

    logger.info("Generating Dimension 2: dim_positions...")
    pos_df = generate_positions(config_loader)

    logger.info("Generating Dimension 3: dim_salary_benchmarks...")
    benchmarks_df = generate_salary_benchmarks(config_loader)

    logger.info("Generating Core Dimension 4: dim_employees (SCD2)...")
    employees_df = generate_employees(config_loader, depts_df, pos_df, benchmarks_df)

    # 3. Generate Fact DataFrames (Correct Topological Sequence)
    logger.info("Generating Fact 1: fact_terminations...")
    terminations_df = generate_terminations(employees_df, config_loader)

    # RECONCILIATION STEP: Update current employee is_active status based on terminations (R01, R04)
    logger.info("Reconciling employee is_active status with terminations...")
    term_emp_ids = set(terminations_df["employee_id"])
    reconciled_mask = (employees_df["is_current_row"] == True) & (employees_df["employee_id"].isin(term_emp_ids))
    employees_df.loc[reconciled_mask, "is_active"] = False
    logger.info(f"[Reconciliation] Marked {reconciled_mask.sum()} current rows as is_active=FALSE. Total inactive current rows: {(employees_df['is_current_row'] & ~employees_df['is_active']).sum()}.")

    logger.info("Generating Fact 2: fact_attendance_logs...")
    attendance_df = generate_attendance_logs(employees_df, terminations_df)

    logger.info("Generating Fact 3: fact_sla_events...")
    sla_df = generate_sla_events(depts_df)

    # 4. Phase 1.5 Comprehensive Business-Rule & Coherence Validation
    datasets_map = {
        "dim_date": date_df,
        "dim_departments": depts_df,
        "dim_positions": pos_df,
        "dim_salary_benchmarks": benchmarks_df,
        "dim_employees": employees_df,
        "fact_attendance_logs": attendance_df,
        "fact_terminations": terminations_df,
        "fact_sla_events": sla_df
    }

    validator = DatasetValidator(datasets_map)
    passed, stats_report = validator.run_all_validations()

    if not passed:
        logger.error("[FATAL] Dataset business rule validation failed! Aborting export.")
        raise ValueError("Dataset validation failed. See log output for details.")

    # 5. Export CSV Files (ONLY IF ALL CRITICAL CHECKS PASS)
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    logger.info(f"Exporting validated datasets to CSV in '{output_dir}'...")
    date_df.to_csv(out_path / "dim_date.csv", index=False, encoding="utf-8")
    depts_df.to_csv(out_path / "dim_departments.csv", index=False, encoding="utf-8")
    pos_df.to_csv(out_path / "dim_positions.csv", index=False, encoding="utf-8")
    benchmarks_df.to_csv(out_path / "dim_salary_benchmarks.csv", index=False, encoding="utf-8")
    employees_df.to_csv(out_path / "dim_employees.csv", index=False, encoding="utf-8")
    attendance_df.to_csv(out_path / "fact_attendance_logs.csv", index=False, encoding="utf-8")
    terminations_df.to_csv(out_path / "fact_terminations.csv", index=False, encoding="utf-8")
    sla_df.to_csv(out_path / "fact_sla_events.csv", index=False, encoding="utf-8")

    with open(out_path / "generation_report.json", "w", encoding="utf-8") as f:
        json.dump(stats_report, f, indent=2)

    logger.info("============================================================")
    logger.info("DATASET GENERATION & VALIDATION COMPLETED SUCCESSFULLY.")
    logger.info("============================================================")

if __name__ == "__main__":
    run_generation_pipeline()

