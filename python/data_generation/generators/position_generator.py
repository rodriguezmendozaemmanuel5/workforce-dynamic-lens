# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.6.0
# Entity Generator 02: Positions Dimension (dim_positions)
# =============================================================================

import pandas as pd
from python.data_generation.utils.config_loader import ConfigLoader
from python.data_generation.utils.logger import setup_logger

logger = setup_logger("position_generator")

def generate_positions(config_loader: ConfigLoader = None) -> pd.DataFrame:
    """Generates dim_positions DataFrame from positions catalog reference data."""
    if config_loader is None:
        config_loader = ConfigLoader()

    catalog = config_loader.load_json_catalog("positions_catalog.json")
    df = pd.DataFrame(catalog)

    columns_order = [
        "position_id", "job_title", "job_family", "job_grade",
        "career_level", "is_critical_position", "is_remote_eligible",
        "market_scarcity_index"
    ]
    df = df[columns_order]

    logger.info(f"Generated dim_positions dataset: {len(df)} positions.")
    return df
