# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.6.0
# Entity Generator 01: Departments Dimension (dim_departments)
# =============================================================================

import pandas as pd
from typing import List, Dict, Any
from python.data_generation.utils.config_loader import ConfigLoader
from python.data_generation.utils.logger import setup_logger

logger = setup_logger("department_generator")

def generate_departments(config_loader: ConfigLoader = None) -> pd.DataFrame:
    """Generates dim_departments DataFrame from departments catalog reference data."""
    if config_loader is None:
        config_loader = ConfigLoader()

    catalog = config_loader.load_json_catalog("departments_catalog.json")
    df = pd.DataFrame(catalog)

    # Required column order matching DDL
    columns_order = [
        "department_id", "department_name", "cost_center_code",
        "vp_responsible", "region", "budget_annual_usd",
        "target_headcount", "strategic_level"
    ]
    df = df[columns_order]

    logger.info(f"Generated dim_departments dataset: {len(df)} departments.")
    return df
