# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.7.0
# ETL Orchestrator: pipeline.py
#
# Usage:
#   --dry-run   Validates CSVs against schema rules. No DB writes.
#   --execute   Runs full load: dim_date → dimensions → facts → audit.
#
# Examples:
#   .venv\Scripts\python.exe -m python.etl.pipeline --dry-run
#   .venv\Scripts\python.exe -m python.etl.pipeline --execute
# =============================================================================

import sys
import time
import argparse
from python.data_generation.utils.logger import setup_logger

from python.etl.connection       import get_engine, test_connection
from python.etl.validation       import DryRunValidator
from python.etl.load_dimensions  import (load_dim_date, load_departments,
                                         load_positions, load_salary_benchmarks,
                                         load_employees)
from python.etl.load_facts       import load_attendance, load_terminations, load_sla_events
from python.etl.lookups          import (build_department_lookup, build_position_lookup,
                                         build_employee_lookup, build_date_lookup)

logger = setup_logger("etl.pipeline")


def run_dry_run() -> bool:
    """Phase 0: validate CSVs without touching the database."""
    logger.info("=" * 60)
    logger.info("MODE: DRY RUN — No database writes will occur.")
    logger.info("=" * 60)
    validator = DryRunValidator(datasets_path="datasets/generated")
    passed, report = validator.run()

    if passed:
        logger.info("✅ Dry run PASSED. Safe to run with --execute.")
    else:
        logger.error("❌ Dry run FAILED. Fix errors above before executing load.")
    return passed


def run_execute() -> None:
    """Full ETL pipeline: dim_date → dimensions → lookups → facts → done."""
    logger.info("=" * 60)
    logger.info("MODE: EXECUTE — Loading data into PostgreSQL.")
    logger.info("=" * 60)
    t_start = time.perf_counter()

    engine = get_engine()
    if not test_connection(engine):
        logger.error("Aborting: cannot connect to PostgreSQL or schema missing.")
        sys.exit(1)

    # ── PHASE 0: Static Date Dimension ─────────────────────────────────
    logger.info("[Phase 0] Loading dim_date (2012–2030)...")
    load_dim_date(engine)

    # ── PHASE 1: Dimension Loading (topological order) ──────────────────
    logger.info("[Phase 1.1] Loading dim_departments...")
    load_departments(engine)
    dept_nk_to_sk = build_department_lookup(engine)

    logger.info("[Phase 1.2] Loading dim_positions...")
    load_positions(engine)
    pos_nk_to_sk = build_position_lookup(engine)

    logger.info("[Phase 1.3] Loading dim_salary_benchmarks...")
    load_salary_benchmarks(engine, pos_nk_to_sk)

    logger.info("[Phase 1.4] Loading dim_employees (SCD2)...")
    load_employees(engine, dept_nk_to_sk, pos_nk_to_sk)
    emp_nk_to_sk = build_employee_lookup(engine)

    # ── PHASE 2: Fact Table Loading (requires all lookups) ──────────────
    date_lookup = build_date_lookup(engine)

    logger.info("[Phase 2.1] Loading fact_attendance_logs (chunked — ~1.8M rows)...")
    load_attendance(engine, emp_nk_to_sk, date_lookup)

    logger.info("[Phase 2.2] Loading fact_terminations...")
    load_terminations(engine, emp_nk_to_sk, date_lookup)

    logger.info("[Phase 2.3] Loading fact_sla_events...")
    load_sla_events(engine, dept_nk_to_sk, date_lookup)

    elapsed = round(time.perf_counter() - t_start, 1)
    logger.info("=" * 60)
    logger.info(f"ETL PIPELINE COMPLETED in {elapsed}s.")
    logger.info("Next step: run sql/analytics/14_validation_queries.sql to verify FK integrity.")
    logger.info("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Workforce Dynamic Lens ETL Pipeline v0.7.0"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run",  action="store_true",
                       help="Validate CSVs without writing to PostgreSQL.")
    group.add_argument("--execute",  action="store_true",
                       help="Load validated data into PostgreSQL.")
    args = parser.parse_args()

    if args.dry_run:
        passed = run_dry_run()
        sys.exit(0 if passed else 1)

    if args.execute:
        run_execute()


if __name__ == "__main__":
    main()
