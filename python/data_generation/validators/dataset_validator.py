# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.7.0
# Phase 1.5: Synthetic Dataset Business Rule & Coherence Validator
# =============================================================================

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, List
from python.data_generation.utils.logger import setup_logger

logger = setup_logger("dataset_validator")

class DatasetValidator:
    def __init__(self, datasets: Dict[str, pd.DataFrame]):
        self.datasets = datasets
        self.report = {}
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_referential_integrity(self) -> bool:
        """Validates that all Natural Key references match parent dimensions."""
        logger.info("--- PHASE 1.5: Validating Referential Integrity (NKs) ---")
        passed = True

        depts_df = self.datasets.get("dim_departments")
        pos_df   = self.datasets.get("dim_positions")
        emp_df   = self.datasets.get("dim_employees")
        att_df   = self.datasets.get("fact_attendance_logs")
        trm_df   = self.datasets.get("fact_terminations")
        sla_df   = self.datasets.get("fact_sla_events")

        # 1. Employees -> Departments
        orphan_depts = set(emp_df["department_id"]) - set(depts_df["department_id"])
        if orphan_depts:
            msg = f"[FAIL] Orphan departments in employees: {orphan_depts}"
            logger.error(msg)
            self.errors.append(msg)
            passed = False
        else:
            logger.info("[PASS] Employees -> Departments referential integrity clean.")

        # 2. Employees -> Positions
        orphan_pos = set(emp_df["position_id"]) - set(pos_df["position_id"])
        if orphan_pos:
            msg = f"[FAIL] Orphan positions in employees: {orphan_pos}"
            logger.error(msg)
            self.errors.append(msg)
            passed = False
        else:
            logger.info("[PASS] Employees -> Positions referential integrity clean.")

        # 3. Attendance -> Employees
        orphan_att_emp = set(att_df["employee_id"]) - set(emp_df["employee_id"])
        if orphan_att_emp:
            msg = f"[FAIL] Orphan employees in attendance logs: {len(orphan_att_emp)}"
            logger.error(msg)
            self.errors.append(msg)
            passed = False
        else:
            logger.info("[PASS] Attendance -> Employees referential integrity clean.")

        # 4. Terminations -> Employees
        orphan_trm_emp = set(trm_df["employee_id"]) - set(emp_df["employee_id"])
        if orphan_trm_emp:
            msg = f"[FAIL] Orphan employees in terminations: {len(orphan_trm_emp)}"
            logger.error(msg)
            self.errors.append(msg)
            passed = False
        else:
            logger.info("[PASS] Terminations -> Employees referential integrity clean.")

        # 5. SLA Events -> Departments
        orphan_sla_dept = set(sla_df["department_id"]) - set(depts_df["department_id"])
        if orphan_sla_dept:
            msg = f"[FAIL] Orphan departments in SLA events: {orphan_sla_dept}"
            logger.error(msg)
            self.errors.append(msg)
            passed = False
        else:
            logger.info("[PASS] SLA Events -> Departments referential integrity clean.")

        return passed

    def validate_termination_employee_consistency(self) -> bool:
        """Validates Business Rules R01, R04, R05, R06 regarding terminations."""
        logger.info("--- PHASE 1.5: Validating Termination & Employment State Consistency ---")
        passed = True

        emp_df = self.datasets.get("dim_employees")
        trm_df = self.datasets.get("fact_terminations")

        current_emps = emp_df[emp_df["is_current_row"] == True].copy()
        term_emp_ids = set(trm_df["employee_id"])

        # R01: Terminated employees MUST be is_active = FALSE on current row
        active_current = current_emps[current_emps["is_active"] == True]
        active_with_term = active_current[active_current["employee_id"].isin(term_emp_ids)]
        if not active_with_term.empty:
            msg = f"[CRITICAL FAIL] R01 Violation: {len(active_with_term)} active current employees have a termination record."
            logger.error(msg)
            self.errors.append(msg)
            passed = False
        else:
            logger.info("[PASS] R01: No active current employees have a termination record.")

        # R04: Inactive current employees MUST have a termination record
        inactive_current = current_emps[current_emps["is_active"] == False]
        inactive_without_term = inactive_current[~inactive_current["employee_id"].isin(term_emp_ids)]
        if not inactive_without_term.empty:
            msg = f"[CRITICAL FAIL] R04 Violation: {len(inactive_without_term)} inactive current employees lack a termination record."
            logger.error(msg)
            self.errors.append(msg)
            passed = False
        else:
            logger.info("[PASS] R04: All inactive current employees have a termination record.")

        # R06: Termination completeness (non-null employee_id, termination_date, termination_type)
        null_terms = trm_df[trm_df["employee_id"].isna() | trm_df["termination_date"].isna() | trm_df["termination_type"].isna()]
        if not null_terms.empty:
            msg = f"[CRITICAL FAIL] R06 Violation: {len(null_terms)} termination records have NULL essential fields."
            logger.error(msg)
            self.errors.append(msg)
            passed = False
        else:
            logger.info("[PASS] R06: All termination records contain non-null core attributes.")

        # R07: Termination date >= hire_date
        merged_trm = trm_df.merge(current_emps[["employee_id", "hire_date"]], on="employee_id", how="left")
        merged_trm["hire_date_dt"] = pd.to_datetime(merged_trm["hire_date"])
        merged_trm["termination_date_dt"] = pd.to_datetime(merged_trm["termination_date"])

        invalid_dates = merged_trm[merged_trm["termination_date_dt"] < merged_trm["hire_date_dt"]]
        if not invalid_dates.empty:
            msg = f"[CRITICAL FAIL] R07 Violation: {len(invalid_dates)} terminations occur before employee hire date."
            logger.error(msg)
            self.errors.append(msg)
            passed = False
        else:
            logger.info("[PASS] R07: All termination dates occur on or after employee hire dates.")

        # Duplicate terminations check
        dupe_terms = trm_df.groupby("employee_id").size()
        dupe_terms = dupe_terms[dupe_terms > 1]
        if not dupe_terms.empty:
            msg = f"[CRITICAL FAIL] R03 Violation: {len(dupe_terms)} employees have multiple termination records."
            logger.error(msg)
            self.errors.append(msg)
            passed = False
        else:
            logger.info("[PASS] R03: All terminated employees have exactly one termination record.")

        return passed

    def validate_scd2_integrity(self) -> bool:
        """Validates Business Rules R08, R09, R10 for SCD Type 2 dimension consistency."""
        logger.info("--- PHASE 1.5: Validating SCD2 Dimensional Integrity ---")
        passed = True

        emp_df = self.datasets.get("dim_employees").copy()

        # R08: Exactly one current row per employee_id
        current_rows = emp_df[emp_df["is_current_row"] == True]
        current_counts = current_rows.groupby("employee_id").size()
        multi_current = current_counts[current_counts > 1]
        missing_current = set(emp_df["employee_id"]) - set(current_rows["employee_id"])

        if not multi_current.empty or missing_current:
            msg = f"[CRITICAL FAIL] R08 Violation: Multiple current rows ({len(multi_current)}) or missing current rows ({len(missing_current)})."
            logger.error(msg)
            self.errors.append(msg)
            passed = False
        else:
            logger.info("[PASS] R08: Exactly one current row per employee_id.")

        # R09: Historical SCD2 rows must have is_active = True
        hist_rows = emp_df[emp_df["is_current_row"] == False]
        hist_inactive = hist_rows[hist_rows["is_active"] == False]
        if not hist_inactive.empty:
            msg = f"[CRITICAL FAIL] R09 Violation: {len(hist_inactive)} historical SCD2 rows marked is_active=False."
            logger.error(msg)
            self.errors.append(msg)
            passed = False
        else:
            logger.info("[PASS] R09: Historical SCD2 rows correctly preserve active employment state.")

        # R10: SCD2 temporal integrity & no overlaps
        emp_df["row_effective_date"] = pd.to_datetime(emp_df["row_effective_date"])
        emp_df["row_expiration_date"] = pd.to_datetime(emp_df["row_expiration_date"])

        # Check effective <= expiration
        invalid_periods = emp_df[emp_df["row_effective_date"] > emp_df["row_expiration_date"]]
        if not invalid_periods.empty:
            msg = f"[CRITICAL FAIL] R10 Violation: {len(invalid_periods)} rows have effective_date > expiration_date."
            logger.error(msg)
            self.errors.append(msg)
            passed = False
        else:
            logger.info("[PASS] R10: All SCD2 rows have row_effective_date <= row_expiration_date.")

        # Check overlaps
        emps_with_hist = emp_df[emp_df["employee_id"].isin(hist_rows["employee_id"].unique())]
        overlaps = 0
        for _, grp in emps_with_hist.groupby("employee_id"):
            if len(grp) < 2:
                continue
            sorted_grp = grp.sort_values("row_effective_date")
            for i in range(len(sorted_grp) - 1):
                if sorted_grp.iloc[i]["row_expiration_date"] >= sorted_grp.iloc[i+1]["row_effective_date"]:
                    overlaps += 1

        if overlaps > 0:
            msg = f"[CRITICAL FAIL] R10 Violation: {overlaps} employee SCD2 periods overlap."
            logger.error(msg)
            self.errors.append(msg)
            passed = False
        else:
            logger.info("[PASS] R10: Zero SCD2 period overlaps detected.")

        return passed

    def validate_attendance_temporal_bounds(self) -> bool:
        """Validates Business Rules R11, R15: No ghost attendance after termination date."""
        logger.info("--- PHASE 1.5: Validating Attendance Temporal Bounds (No Ghost Attendance) ---")
        passed = True

        att_df = self.datasets.get("fact_attendance_logs").copy()
        trm_df = self.datasets.get("fact_terminations").copy()

        att_df["date_key_dt"] = pd.to_datetime(att_df["date_key"])
        trm_df["termination_date_dt"] = pd.to_datetime(trm_df["termination_date"])

        merged = att_df.merge(trm_df[["employee_id", "termination_date_dt"]], on="employee_id", how="inner")
        ghost_records = merged[merged["date_key_dt"] > merged["termination_date_dt"]]

        if not ghost_records.empty:
            msg = f"[CRITICAL FAIL] R11/R15 Violation: {len(ghost_records)} ghost attendance records exist after employee termination date."
            logger.error(msg)
            self.errors.append(msg)
            passed = False
        else:
            logger.info("[PASS] R11/R15: Zero ghost attendance records found after termination date.")

        return passed

    def validate_statistical_distributions(self) -> Dict[str, Any]:
        """Validates HR business metrics and distributions using proper semantics (R02, R11, R12)."""
        logger.info("--- PHASE 1.5: Validating HR Statistical Distributions ---")
        emp_df = self.datasets.get("dim_employees")
        att_df = self.datasets.get("fact_attendance_logs")
        trm_df = self.datasets.get("fact_terminations")

        # R02: Active Headcount = current row AND is_active = TRUE
        current_rows = emp_df[emp_df["is_current_row"] == True]
        active_emps = current_rows[current_rows["is_active"] == True]
        inactive_emps = current_rows[current_rows["is_active"] == False]

        # 1. Salary Distribution (Active employees)
        salaries = active_emps["annual_base_salary_usd"]
        salary_stats = {
            "min_usd": float(salaries.min()) if not salaries.empty else 0.0,
            "max_usd": float(salaries.max()) if not salaries.empty else 0.0,
            "mean_usd": float(round(salaries.mean(), 2)) if not salaries.empty else 0.0,
            "median_usd": float(round(salaries.median(), 2)) if not salaries.empty else 0.0
        }
        logger.info(f"Active Salary Stats: Mean=${salary_stats['mean_usd']:,}, Median=${salary_stats['median_usd']:,}")

        # 2. Country Headcount Distribution
        country_dist = active_emps["country_code"].value_counts(normalize=True).to_dict()
        logger.info(f"Active Country Headcount Distribution: {country_dist}")

        # 3. Absence Rate
        total_att_days = len(att_df)
        unplanned_absences = att_df["is_unplanned_absence"].sum()
        absence_rate = round((unplanned_absences / total_att_days) * 100, 2) if total_att_days > 0 else 0.0
        logger.info(f"Unplanned Absence Rate: {absence_rate}% of total attendance days.")

        # 4. Attrition Metrics
        term_count = len(trm_df)
        total_historical_pop = len(current_rows)
        turnover_ratio_of_total = round((term_count / total_historical_pop) * 100, 2) if total_historical_pop > 0 else 0.0
        logger.info(f"Historical Offboarding Count: {term_count} ({turnover_ratio_of_total}% of historical population).")
        logger.info(f"Current Headcount Snapshot: Active={len(active_emps)}, Inactive={len(inactive_emps)}.")

        self.report = {
            "historical_employee_population": len(current_rows),
            "current_active_headcount": len(active_emps),
            "current_inactive_headcount": len(inactive_emps),
            "total_employee_records_scd2": len(emp_df),
            "total_terminations": term_count,
            "salary_stats": salary_stats,
            "country_distribution": country_dist,
            "unplanned_absence_rate_pct": absence_rate,
            "historical_turnover_ratio_pct": turnover_ratio_of_total,
            "validation_errors_count": len(self.errors)
        }
        return self.report

    def run_all_validations(self) -> Tuple[bool, Dict[str, Any]]:
        """Runs the entire validation suite and returns (passed, report)."""
        logger.info("============================================================")
        logger.info("RUNNING FULL SYNTHETIC DATASET VALIDATION SUITE v0.7.0")
        logger.info("============================================================")
        
        fk_ok = self.validate_referential_integrity()
        trm_ok = self.validate_termination_employee_consistency()
        scd2_ok = self.validate_scd2_integrity()
        att_ok = self.validate_attendance_temporal_bounds()
        stats = self.validate_statistical_distributions()

        passed = fk_ok and trm_ok and scd2_ok and att_ok and (len(self.errors) == 0)

        if passed:
            logger.info("✅ ALL DATASET BUSINESS RULES AND INTEGRITY CHECKS PASSED.")
        else:
            logger.error(f"❌ DATASET VALIDATION FAILED with {len(self.errors)} critical errors.")
            for err in self.errors:
                logger.error(f"   - {err}")

        logger.info("============================================================")
        return passed, stats

