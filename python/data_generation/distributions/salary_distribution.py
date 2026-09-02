# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.6.0
# Statistical Distribution: Salary & Compa-Ratio Sampling
# =============================================================================

import numpy as np
from python.data_generation.utils.random_state import SeedManager

def generate_salary_around_midpoint(midpoint_usd: float, scarcity_index: float) -> float:
    """
    Generates realistic employee salary around market midpoint.
    Higher scarcity index slightly skews salaries above midpoint.
    """
    rng = SeedManager.get_rng()
    # Log-normal distribution centered around 1.0 (Compa-Ratio ~ 1.0)
    skew = (scarcity_index - 1.0) * 0.05
    ratio = rng.lognormal(mean=0.0 + skew, sigma=0.12)
    ratio = np.clip(ratio, 0.75, 1.35)  # Restrict to reasonable Compa-Ratio bounds
    return round(midpoint_usd * ratio, 2)
