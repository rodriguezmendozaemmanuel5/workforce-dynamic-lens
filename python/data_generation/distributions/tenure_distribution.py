# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.6.0
# Statistical Distribution: Tenure & Hire Date Sampling
# =============================================================================

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from python.data_generation.utils.random_state import SeedManager

def generate_hire_date(start_year: int = 2012, max_date: datetime = None) -> datetime:
    """Generates realistic employee hire date with exponential decay towards recent dates."""
    rng = SeedManager.get_rng()
    if max_date is None:
        max_date = datetime(2025, 12, 31)

    # Exponential distribution favoring more recent hires (0 to 13 years tenure)
    tenure_years = rng.exponential(scale=3.8)
    tenure_years = min(tenure_years, 13.0)

    hire_date = max_date - timedelta(days=int(tenure_years * 365.25))
    if hire_date < datetime(start_year, 1, 1):
        hire_date = datetime(start_year, 1, 1) + timedelta(days=int(rng.uniform(0, 365)))
    
    return hire_date
