# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.6.0
# Statistical Distribution: Performance & Potential 9-Box Grid Sampling
# =============================================================================

import numpy as np
from typing import Tuple, Optional
from python.data_generation.utils.random_state import SeedManager

def generate_performance_and_potential(tenure_months: float) -> Tuple[Optional[float], Optional[str]]:
    """
    Generates performance rating (1.00-5.00) and 9-box potential rating.
    Employees with tenure < 6 months have NULL (BR-03 / DQ-RNG-02).
    """
    if tenure_months < 6.0:
        return None, None

    rng = SeedManager.get_rng()
    # Normal distribution centered around 3.4 (typical enterprise rating curve)
    rating = round(rng.normal(loc=3.4, scale=0.65), 2)
    rating = max(1.00, min(5.00, rating))

    # Potential mapping correlated with performance rating
    if rating >= 4.2:
        potential = rng.choice(['Alto', 'Top Talent'], p=[0.4, 0.6])
    elif rating >= 3.2:
        potential = rng.choice(['Medio', 'Alto'], p=[0.7, 0.3])
    else:
        potential = rng.choice(['Bajo', 'Medio'], p=[0.8, 0.2])

    return rating, potential
