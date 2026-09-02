# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.6.0
# Entity Generator 03: Salary Benchmarks Dimension (dim_salary_benchmarks)
# =============================================================================

import pandas as pd
from python.data_generation.utils.config_loader import ConfigLoader
from python.data_generation.utils.logger import setup_logger

logger = setup_logger("benchmark_generator")

def generate_salary_benchmarks(config_loader: ConfigLoader = None) -> pd.DataFrame:
    """Generates dim_salary_benchmarks DataFrame with active benchmark flag (is_current_benchmark)."""
    if config_loader is None:
        config_loader = ConfigLoader()

    catalog = config_loader.load_json_catalog("salary_benchmarks.json")
    df = pd.DataFrame(catalog)

    # Set is_current_benchmark = True for latest benchmarks (AUD-11)
    df["is_current_benchmark"] = True

    columns_order = [
        "benchmark_id", "position_id", "country_code",
        "market_min_salary_usd", "market_midpoint_salary_usd",
        "market_max_salary_usd", "survey_provider",
        "effective_year", "is_current_benchmark"
    ]
    df = df[columns_order]

    logger.info(f"Generated dim_salary_benchmarks dataset: {len(df)} benchmarks.")
    return df
