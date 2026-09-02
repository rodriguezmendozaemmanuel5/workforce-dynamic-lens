# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.6.0
# ETL Layer: Pre-Load Dry-Run Validation
# Validates CSV data against schema rules BEFORE any INSERT to PostgreSQL.
# =============================================================================

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
from python.data_generation.utils.logger import setup_logger

logger = setup_logger("etl.validation")


class DryRunValidator:
    """
    Validates all CSV datasets against PostgreSQL schema rules (types, ranges, FKs)
    without performing any database writes.

    Usage:
        validator = DryRunValidator(datasets_path="datasets/generated")
        passed, report = validator.run()
        if not passed:
            sys.exit(1)
    """

    def __init__(self, datasets_path: str = "datasets/generated"):
        self.path = Path(datasets_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def _load(self, filename: str) -> pd.DataFrame:
        return pd.read_csv(self.path / filename, low_memory=False)

    # ------------------------------------------------------------------
    # 1. Type validation
    # ------------------------------------------------------------------
    def validate_types(self, df: pd.DataFrame, table: str,
                       numeric_cols: List[str], date_cols: List[str]) -> bool:
        ok = True
        for col in numeric_cols:
            if col in df.columns:
                non_numeric = pd.to_numeric(df[col], errors="coerce").isna() & df[col].notna()
                if non_numeric.any():
                    self.errors.append(f"[{table}] Non-numeric values in '{col}': {non_numeric.sum()} rows")
                    ok = False
        for col in date_cols:
            if col in df.columns:
                non_date = pd.to_datetime(df[col], errors="coerce").isna() & df[col].notna()
                if non_date.any():
                    self.errors.append(f"[{table}] Non-date values in '{col}': {non_date.sum()} rows")
                    ok = False
        return ok

    # ------------------------------------------------------------------
    # 2. NOT NULL validation
    # ------------------------------------------------------------------
    def validate_not_null(self, df: pd.DataFrame, table: str,
                          required_cols: List[str]) -> bool:
        ok = True
        for col in required_cols:
            if col in df.columns and df[col].isna().any():
                count = df[col].isna().sum()
                self.errors.append(f"[{table}] NULL in NOT NULL column '{col}': {count} rows")
                ok = False
        return ok

    # ------------------------------------------------------------------
    # 3. Range validation (CHECK constraints)
    # ------------------------------------------------------------------
    def validate_ranges(self, df: pd.DataFrame, table: str) -> bool:
        ok = True
        if table == "dim_employees":
            sal = pd.to_numeric(df.get("annual_base_salary_usd", pd.Series()), errors="coerce")
            bad = ((sal <= 0) | (sal > 300000)) & sal.notna()
            if bad.any():
                self.errors.append(f"[dim_employees] annual_base_salary_usd out of range (0, 300000]: {bad.sum()} rows")
                ok = False
            perf = pd.to_numeric(df.get("performance_rating", pd.Series()), errors="coerce")
            bad_perf = ((perf < 1.0) | (perf > 5.0)) & perf.notna()
            if bad_perf.any():
                self.errors.append(f"[dim_employees] performance_rating out of range [1, 5]: {bad_perf.sum()} rows")
                ok = False

        if table == "fact_attendance_logs":
            planned = pd.to_numeric(df.get("planned_hours", pd.Series()), errors="coerce")
            bad = ((planned < 0) | (planned > 12)) & planned.notna()
            if bad.any():
                self.errors.append(f"[fact_attendance_logs] planned_hours out of [0,12]: {bad.sum()} rows")
                ok = False
            actual = pd.to_numeric(df.get("actual_hours_worked", pd.Series()), errors="coerce")
            bad2 = ((actual < 0) | (actual > 16)) & actual.notna()
            if bad2.any():
                self.errors.append(f"[fact_attendance_logs] actual_hours_worked out of [0,16]: {bad2.sum()} rows")
                ok = False

        return ok

    # ------------------------------------------------------------------
    # 4. Referential integrity (NK cross-check between CSVs)
    # ------------------------------------------------------------------
    def validate_fk_integrity(self) -> bool:
        logger.info("[DryRun] Checking cross-CSV referential integrity...")
        ok = True

        depts  = self._load("dim_departments.csv")["department_id"].tolist()
        pos    = self._load("dim_positions.csv")["position_id"].tolist()
        emps   = self._load("dim_employees.csv")
        att    = self._load("fact_attendance_logs.csv")
        trm    = self._load("fact_terminations.csv")
        sla    = self._load("fact_sla_events.csv")

        # Employees → Departments
        orphans = set(emps["department_id"]) - set(depts)
        if orphans:
            self.errors.append(f"[dim_employees] Unknown department_ids: {orphans}")
            ok = False

        # Employees → Positions
        orphans = set(emps["position_id"]) - set(pos)
        if orphans:
            self.errors.append(f"[dim_employees] Unknown position_ids: {orphans}")
            ok = False

        # Attendance → Employees
        emp_ids = set(emps["employee_id"])
        orphans = set(att["employee_id"]) - emp_ids
        if orphans:
            self.errors.append(f"[fact_attendance_logs] {len(orphans)} unknown employee_ids")
            ok = False

        # Terminations → Employees
        orphans = set(trm["employee_id"]) - emp_ids
        if orphans:
            self.errors.append(f"[fact_terminations] {len(orphans)} unknown employee_ids")
            ok = False

        # SLA Events → Departments
        orphans = set(sla["department_id"]) - set(depts)
        if orphans:
            self.errors.append(f"[fact_sla_events] Unknown department_ids: {orphans}")
            ok = False

        return ok

    # ------------------------------------------------------------------
    # 5. Grain uniqueness (duplicate detection)
    # ------------------------------------------------------------------
    def validate_grain(self) -> bool:
        logger.info("[DryRun] Checking grain uniqueness constraints...")
        ok = True

        att = self._load("fact_attendance_logs.csv")
        dupes_att = att.duplicated(subset=["employee_id", "date_key"]).sum()
        if dupes_att > 0:
            self.errors.append(f"[fact_attendance_logs] {dupes_att} duplicate (employee_id, date_key) rows — violates UNIQUE constraint")
            ok = False

        trm = self._load("fact_terminations.csv")
        dupes_trm = trm.duplicated(subset=["employee_id", "termination_date"]).sum()
        if dupes_trm > 0:
            self.errors.append(f"[fact_terminations] {dupes_trm} duplicate (employee_id, termination_date) rows")
            ok = False

        # SCD2: only one is_current_row=True per employee_id
        emps = self._load("dim_employees.csv")
        current = emps[emps["is_current_row"] == True]
        scd2_dupes = current.duplicated(subset=["employee_id"]).sum()
        if scd2_dupes > 0:
            self.errors.append(f"[dim_employees] {scd2_dupes} employees with multiple is_current_row=True — SCD2 violation")
            ok = False

        return ok

    # ------------------------------------------------------------------
    # 6. Birth date validation (cannot use CURRENT_DATE in PG CHECK)
    # ------------------------------------------------------------------
    def validate_birth_dates(self) -> bool:
        emps = self._load("dim_employees.csv")
        emps["birth_date"] = pd.to_datetime(emps["birth_date"])
        cutoff = pd.Timestamp.today() - pd.DateOffset(years=18)
        invalid = emps[emps["birth_date"] > cutoff]
        if not invalid.empty:
            self.warnings.append(f"[dim_employees] {len(invalid)} employees under 18 years old at today's date.")
        return True  # WARNING only, not a blocking error

    # ------------------------------------------------------------------
    # 7. Business Rule Consistency (R01, R04, R07)
    # ------------------------------------------------------------------
    def validate_termination_consistency(self) -> bool:
        logger.info("[DryRun] Checking termination business rules & state consistency...")
        ok = True
        emps = self._load("dim_employees.csv")
        trm = self._load("fact_terminations.csv")

        current = emps[emps["is_current_row"] == True]
        trm_emp_ids = set(trm["employee_id"])

        # R01: Terminated employees must be is_active = False
        active_current = current[current["is_active"] == True]
        active_with_term = active_current[active_current["employee_id"].isin(trm_emp_ids)]
        if not active_with_term.empty:
            self.errors.append(f"[dim_employees] R01 Violation: {len(active_with_term)} active current employees have a termination record.")
            ok = False

        # R04: Inactive current employees must have a termination record
        inactive_current = current[current["is_active"] == False]
        inactive_without_term = inactive_current[~inactive_current["employee_id"].isin(trm_emp_ids)]
        if not inactive_without_term.empty:
            self.errors.append(f"[dim_employees] R04 Violation: {len(inactive_without_term)} inactive current employees lack a termination record.")
            ok = False

        # R07: Termination date >= hire_date
        merged_trm = trm.merge(current[["employee_id", "hire_date"]], on="employee_id", how="left")
        merged_trm["hire_dt"] = pd.to_datetime(merged_trm["hire_date"])
        merged_trm["term_dt"] = pd.to_datetime(merged_trm["termination_date"])
        invalid_dates = merged_trm[merged_trm["term_dt"] < merged_trm["hire_dt"]]
        if not invalid_dates.empty:
            self.errors.append(f"[fact_terminations] R07 Violation: {len(invalid_dates)} terminations occur before hire_date.")
            ok = False

        return ok

    # ------------------------------------------------------------------
    # 8. SCD2 Integrity (R09, R10)
    # ------------------------------------------------------------------
    def validate_scd2_integrity(self) -> bool:
        logger.info("[DryRun] Checking SCD2 historical state & temporal boundaries...")
        ok = True
        emps = self._load("dim_employees.csv")

        # R09: Historical rows should preserve is_active = True
        hist_rows = emps[emps["is_current_row"] == False]
        hist_inactive = hist_rows[hist_rows["is_active"] == False]
        if not hist_inactive.empty:
            self.errors.append(f"[dim_employees] R09 Violation: {len(hist_inactive)} historical SCD2 rows marked is_active=False.")
            ok = False

        # R10: Effective <= Expiration and zero overlaps
        emps["eff_dt"] = pd.to_datetime(emps["row_effective_date"])
        emps["exp_dt"] = pd.to_datetime(emps["row_expiration_date"])

        invalid_bounds = emps[emps["eff_dt"] > emps["exp_dt"]]
        if not invalid_bounds.empty:
            self.errors.append(f"[dim_employees] R10 Violation: {len(invalid_bounds)} rows have effective_date > expiration_date.")
            ok = False

        emps_with_hist = emps[emps["employee_id"].isin(hist_rows["employee_id"].unique())]
        overlaps = 0
        for _, grp in emps_with_hist.groupby("employee_id"):
            if len(grp) < 2:
                continue
            sorted_grp = grp.sort_values("eff_dt")
            for i in range(len(sorted_grp) - 1):
                if sorted_grp.iloc[i]["exp_dt"] >= sorted_grp.iloc[i+1]["eff_dt"]:
                    overlaps += 1

        if overlaps > 0:
            self.errors.append(f"[dim_employees] R10 Violation: {overlaps} employee SCD2 periods overlap.")
            ok = False

        return ok

    # ------------------------------------------------------------------
    # 9. Attendance Temporal Bounds (R11, R15)
    # ------------------------------------------------------------------
    def validate_attendance_bounds(self) -> bool:
        logger.info("[DryRun] Checking attendance temporal bounds (no ghost attendance)...")
        ok = True
        att = self._load("fact_attendance_logs.csv")
        trm = self._load("fact_terminations.csv")

        att["att_dt"] = pd.to_datetime(att["date_key"])
        trm["term_dt"] = pd.to_datetime(trm["termination_date"])

        merged = att.merge(trm[["employee_id", "term_dt"]], on="employee_id", how="inner")
        ghosts = merged[merged["att_dt"] > merged["term_dt"]]
        if not ghosts.empty:
            self.errors.append(f"[fact_attendance_logs] R11/R15 Violation: {len(ghosts)} ghost attendance records after termination date.")
            ok = False

        return ok

    # ------------------------------------------------------------------
    # Orchestrator
    # ------------------------------------------------------------------
    def run(self) -> Tuple[bool, dict]:
        logger.info("=" * 60)
        logger.info("DRY RUN VALIDATION — Workforce Dynamic Lens ETL")
        logger.info("=" * 60)

        emps_df = self._load("dim_employees.csv")

        self.validate_types(emps_df, "dim_employees",
                            numeric_cols=["annual_base_salary_usd", "base_salary_orig",
                                          "fully_loaded_cost_usd", "performance_rating"],
                            date_cols=["hire_date", "birth_date",
                                       "row_effective_date", "row_expiration_date"])

        self.validate_not_null(emps_df, "dim_employees",
                               required_cols=["employee_id", "first_name", "last_name",
                                              "work_email", "gender", "hire_date",
                                              "department_id", "position_id",
                                              "annual_base_salary_usd"])

        self.validate_ranges(emps_df, "dim_employees")
        self.validate_fk_integrity()
        self.validate_grain()
        self.validate_birth_dates()
        self.validate_termination_consistency()
        self.validate_scd2_integrity()
        self.validate_attendance_bounds()

        passed = len(self.errors) == 0
        report = {
            "passed": passed,
            "errors": self.errors,
            "warnings": self.warnings
        }

        if passed:
            logger.info(f"[DryRun] ALL CHECKS PASSED. {len(self.warnings)} warnings.")
        else:
            logger.error(f"[DryRun] FAILED — {len(self.errors)} blocking errors, {len(self.warnings)} warnings.")
            for e in self.errors:
                logger.error(f"  ✗ {e}")
        for w in self.warnings:
            logger.warning(f"  ⚠ {w}")

        logger.info("=" * 60)
        return passed, report

