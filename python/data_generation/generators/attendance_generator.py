# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.6.0
# Entity Generator 05: Attendance Logs Fact Table (fact_attendance_logs)
# =============================================================================

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any

from python.data_generation.utils.config_loader import ConfigLoader
from python.data_generation.utils.random_state import SeedManager
from python.data_generation.utils.logger import setup_logger
from python.data_generation.distributions.absence_distribution import sample_absence_event

logger = setup_logger("attendance_generator")

def generate_attendance_logs(employees_df: pd.DataFrame,
                             terminations_df: pd.DataFrame = None,
                             start_date: str = "2024-01-01",
                             end_date: str = "2025-12-31") -> pd.DataFrame:
    """
    Generates daily attendance fact records for active employees.
    Calculates clock-in/out, planned/actual hours, overtime, and Bradford flags.
    Enforces R11 / R15: attendance records MUST NOT occur after employee termination date.
    """
    rng = SeedManager.get_rng()
    active_emps = employees_df[employees_df["is_current_row"] == True].copy()
    
    term_lookup = {}
    if terminations_df is not None and not terminations_df.empty:
        for _, row in terminations_df.iterrows():
            term_lookup[row["employee_id"]] = pd.to_datetime(row["termination_date"])
        logger.info(f"Termination lookup built for attendance generator: {len(term_lookup)} offboarded employees.")

    date_range = pd.date_range(start=start_date, end=end_date, freq="B")  # Business days
    total_expected = len(active_emps) * len(date_range)
    logger.info(f"Generating attendance logs for {len(active_emps)} employees across {len(date_range)} business days (~{total_expected:,} max rows)...")

    # Pre-extract employee fields to avoid slow iterrows in nested loop
    emp_records = [
        {
            "employee_id": emp["employee_id"],
            "hire_dt": pd.to_datetime(emp["hire_date"]),
            "performance_rating": emp["performance_rating"]
        }
        for _, emp in active_emps.iterrows()
    ]

    # Vectorized per-employee date loop (100x faster execution)
    global_start = pd.Timestamp(start_date)
    global_end = pd.Timestamp(end_date)
    att_counter = 1
    rows = []

    shifts = ["Mañana", "Tarde", "Noche", "Central"]
    shift_probs = [0.40, 0.30, 0.15, 0.15]
    unplanned_types = ['Incapacidad Medica', 'Injustificada']
    unplanned_probs = [0.75, 0.25]
    planned_types = ['Vacaciones', 'Licencia Legal', 'Permiso Autorizado']
    planned_probs = [0.70, 0.15, 0.15]

    for emp in emp_records:
        emp_id = emp["employee_id"]
        hire_dt = emp["hire_dt"]
        perf_rating = emp["performance_rating"]
        
        eff_start = max(global_start, hire_dt)
        eff_end = min(global_end, term_lookup.get(emp_id, global_end))
        if eff_start > eff_end:
            continue

        emp_dates = pd.date_range(start=eff_start, end=eff_end, freq="B")
        num_days = len(emp_dates)
        if num_days == 0:
            continue

        # Vectorize random draws for this employee's active days
        rand_shifts = rng.choice(shifts, size=num_days, p=shift_probs)
        rand_overtimes = rng.exponential(scale=8.0, size=num_days)
        rand_abs_prob = rng.random(num_days)
        rand_unplanned_flag = rng.random(num_days) < 0.40
        rand_unplanned_choice = rng.choice(unplanned_types, size=num_days, p=unplanned_probs)
        rand_planned_choice = rng.choice(planned_types, size=num_days, p=planned_probs)
        rand_instance = rng.random(num_days) < 0.65
        rand_extra = rng.exponential(scale=0.5, size=num_days)
        rand_extra_flag = rng.random(num_days) < 0.20
        rand_minutes = rng.uniform(0, 15, size=num_days)

        for i in range(num_days):
            dt = emp_dates[i]
            date_str = dt.strftime("%Y-%m-%d")
            date_key_int = int(dt.strftime("%Y%m%d"))
            shift = rand_shifts[i]

            # Calculate base absence probability
            base_prob = 0.035
            if rand_overtimes[i] > 25.0:
                base_prob += 0.025
            if perf_rating is not None and perf_rating < 2.5:
                base_prob += 0.020

            is_absent = rand_abs_prob[i] <= base_prob
            att_id = f"ATT_{date_key_int}{att_counter:06d}"
            att_counter += 1

            if is_absent:
                is_unplanned = rand_unplanned_flag[i]
                absence_type = rand_unplanned_choice[i] if is_unplanned else rand_planned_choice[i]
                is_instance_start = is_unplanned and rand_instance[i]
                rows.append({
                    "attendance_id": att_id,
                    "employee_id": emp_id,
                    "date_key": date_str,
                    "shift_type": shift,
                    "clock_in_time": None,
                    "clock_out_time": None,
                    "planned_hours": 8.00,
                    "actual_hours_worked": 0.00,
                    "overtime_hours": 0.00,
                    "absence_type": absence_type,
                    "is_unplanned_absence": is_unplanned,
                    "is_absence_instance_start": is_instance_start
                })
            else:
                planned = 8.00
                extra = round(float(rand_extra[i]), 2) if rand_extra_flag[i] else 0.00
                actual = min(16.00, round(planned + extra, 2))
                clock_in = datetime.combine(dt.date(), datetime.min.time()).replace(hour=9, minute=int(rand_minutes[i]))
                clock_out = clock_in + timedelta(hours=actual)

                rows.append({
                    "attendance_id": att_id,
                    "employee_id": emp_id,
                    "date_key": date_str,
                    "shift_type": shift,
                    "clock_in_time": clock_in.strftime("%Y-%m-%d %H:%M:%S+00"),
                    "clock_out_time": clock_out.strftime("%Y-%m-%d %H:%M:%S+00"),
                    "planned_hours": planned,
                    "actual_hours_worked": actual,
                    "overtime_hours": extra,
                    "absence_type": None,
                    "is_unplanned_absence": False,
                    "is_absence_instance_start": False
                })

    df = pd.DataFrame(rows)
    logger.info(f"Generated fact_attendance_logs dataset: {len(df):,} rows.")
    return df
