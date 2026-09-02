# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.6.0
# Entity Generator 07: SLA Events Fact Table (fact_sla_events)
# =============================================================================

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any

from python.data_generation.utils.config_loader import ConfigLoader
from python.data_generation.utils.random_state import SeedManager
from python.data_generation.utils.logger import setup_logger

logger = setup_logger("sla_generator")

BREACH_TYPES = [
    "Retraso en Respuesta a Incidente Crítico",
    "Falta de Personal en Turno Nocturno",
    "Incumplimiento de Tiempo de Resolución",
    "Ausencia de Cobertura en Soporte B2B"
]

def generate_sla_events(depts_df: pd.DataFrame,
                        start_date: str = "2024-01-01",
                        end_date: str = "2025-12-31") -> pd.DataFrame:
    """
    Generates fact_sla_events records tracking contract penalty costs
    and staffing deficit attribution (BR-14 / KPI-FIN-02).
    """
    rng = SeedManager.get_rng()
    ops_depts = depts_df[depts_df["strategic_level"].isin(["Operation Critical", "Core Revenue"])]["department_id"].tolist()

    date_range = pd.date_range(start=start_date, end=end_date, freq="W")  # Sample weekly potential incidents
    rows = []
    sla_counter = 1

    for dt in date_range:
        if rng.random() > 0.40:
            continue  # 40% probability of breach incident in any week

        dept_id = rng.choice(ops_depts)
        shift_id = rng.choice(["Mañana", "Tarde", "Noche"], p=[0.20, 0.30, 0.50])
        breach_type = rng.choice(BREACH_TYPES)
        
        hours_delayed = round(rng.uniform(1.0, 14.5), 2)
        penalty_cost = round(hours_delayed * rng.uniform(850.0, 2500.0), 2)

        # Attributed to staffing deficit (higher probability in night shift breaches)
        attributed_deficit = (shift_id == "Noche") or (rng.random() < 0.60)

        contract_id = f"CTR_{rng.integers(10000, 99999)}"
        sla_id = f"SLA_{dt.strftime('%Y%m%d')}{sla_counter:03d}"
        sla_counter = (sla_counter % 999) + 1

        rows.append({
            "sla_event_id": sla_id,
            "department_id": dept_id,
            "event_date": dt.strftime("%Y-%m-%d"),
            "client_contract_id": contract_id,
            "shift_id": shift_id,
            "breach_type": breach_type,
            "hours_delayed": hours_delayed,
            "penalty_cost_usd": penalty_cost,
            "attributed_to_staffing_deficit": attributed_deficit
        })

    df = pd.DataFrame(rows)
    logger.info(f"Generated fact_sla_events dataset: {len(df)} breach records.")
    return df
