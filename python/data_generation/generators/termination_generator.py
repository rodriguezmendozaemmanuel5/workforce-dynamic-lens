# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.6.0
# Entity Generator 06: Terminations Fact Table (fact_terminations)
# =============================================================================

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any

from python.data_generation.utils.config_loader import ConfigLoader
from python.data_generation.utils.random_state import SeedManager
from python.data_generation.utils.logger import setup_logger

logger = setup_logger("termination_generator")

HRIS_REASONS = [
    "Desarrollo Profesional",
    "Motivos Personales",
    "Oferta Externa Superior",
    "Reestructuración Operativa",
    "Bajo Desempeño"
]

def generate_terminations(employees_df: pd.DataFrame,
                          config_loader: ConfigLoader = None) -> pd.DataFrame:
    """
    Generates fact_terminations records for historical offboardings.
    Implements proxy exit reason reclassification (BR-23 / FR-09).
    """
    if config_loader is None:
        config_loader = ConfigLoader()

    config = config_loader.load_yaml_config()
    target_terms = config["company_scale"]["historical_terminations_target"]
    rng = SeedManager.get_rng()

    active_emps = employees_df[employees_df["is_current_row"] == True].copy()
    
    # Select subset of employees to terminate
    sampled_indices = rng.choice(len(active_emps), size=min(target_terms, len(active_emps)), replace=False)
    term_emps = active_emps.iloc[sampled_indices]

    rows = []
    
    for i, (_, emp) in enumerate(term_emps.iterrows(), start=1):
        emp_id = emp["employee_id"]
        hire_dt = pd.to_datetime(emp["hire_date"])
        annual_usd = emp["annual_base_salary_usd"]
        perf_rating = emp["performance_rating"] if emp["performance_rating"] is not None else 3.0

        # Termination date between hire date + 6 months and end of 2025
        min_term_dt = hire_dt + timedelta(days=180)
        max_term_dt = datetime(2025, 12, 31)

        if min_term_dt >= max_term_dt:
            term_dt = max_term_dt
        else:
            days_span = (max_term_dt - min_term_dt).days
            term_dt = min_term_dt + timedelta(days=int(rng.uniform(0, days_span)))

        term_type = rng.choice(["Voluntaria", "Involuntaria", "Jubilacion", "Mutual Acuerdo"], p=[0.65, 0.25, 0.05, 0.05])
        hris_reason = rng.choice(HRIS_REASONS)

        # Proxy Reclassification Logic (BR-23):
        # If HRIS = 'Desarrollo Profesional' but Compa-Ratio < 0.85 -> 'Inconformidad Salarial (Proxy)'
        # If HRIS = 'Desarrollo Profesional' and random burnout trigger -> 'Burnout / Agotamiento (Proxy)'
        if hris_reason == "Desarrollo Profesional":
            rand_val = rng.random()
            if rand_val < 0.45:
                proxy_reason = "Inconformidad Salarial (Proxy)"
            elif rand_val < 0.75:
                proxy_reason = "Burnout / Agotamiento (Proxy)"
            else:
                proxy_reason = "Desarrollo Profesional (Verificado)"
        else:
            proxy_reason = hris_reason

        # Severance cost (higher for involuntary terminations)
        if term_type == "Involuntaria":
            severance_usd = round(annual_usd * rng.uniform(0.25, 0.50), 2)
        else:
            severance_usd = 0.00

        notice_days = int(rng.choice([0, 15, 30, 60, 90], p=[0.20, 0.20, 0.40, 0.15, 0.05]))
        is_regrettable = (term_type == "Voluntaria") and (perf_rating >= 3.8)

        trm_id = f"TRM_{term_dt.strftime('%Y%m%d')}{i:04d}"

        rows.append({
            "termination_id": trm_id,
            "employee_id": emp_id,
            "termination_date": term_dt.strftime("%Y-%m-%d"),
            "termination_type": term_type,
            "hris_exit_reason": hris_reason,
            "proxy_reclassified_reason": proxy_reason,
            "severance_cost_usd": severance_usd,
            "notice_period_days": notice_days,
            "is_regrettable_attrition": is_regrettable
        })

    df = pd.DataFrame(rows)
    logger.info(f"Generated fact_terminations dataset: {len(df)} offboarding events.")
    return df
