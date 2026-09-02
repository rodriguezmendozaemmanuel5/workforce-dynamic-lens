# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.6.0
# Statistical Distribution: Absence Sampling & Bradford Factor Trigger
# =============================================================================

import numpy as np
from typing import Tuple, Optional
from python.data_generation.utils.random_state import SeedManager

ABSENCE_TYPES_UNPLANNED = ['Incapacidad Medica', 'Injustificada']
ABSENCE_TYPES_PLANNED = ['Vacaciones', 'Licencia Legal', 'Permiso Autorizado']

def sample_absence_event(performance_rating: Optional[float],
                         overtime_hours_30d: float) -> Tuple[bool, Optional[str], bool]:
    """
    Samples absence occurrence for a daily attendance record.
    Correlations:
    - Lower performance rating slightly increases unplanned absence probability.
    - Higher recent overtime hours increases unplanned absence probability (burnout).
    
    Returns: (is_absence, absence_type, is_unplanned)
    """
    rng = SeedManager.get_rng()
    
    base_absence_prob = 0.035  # ~3.5% baseline absence on any given day
    
    # Overtime burnout risk adjustment
    if overtime_hours_30d > 25.0:
        base_absence_prob += 0.025
    
    # Low performance disengagement risk adjustment
    if performance_rating is not None and performance_rating < 2.5:
        base_absence_prob += 0.020

    if rng.random() > base_absence_prob:
        return False, None, False  # Present

    # Sample absence type (60% planned vs 40% unplanned)
    is_unplanned = rng.random() < 0.40
    
    if is_unplanned:
        absence_type = rng.choice(ABSENCE_TYPES_UNPLANNED, p=[0.75, 0.25])
    else:
        absence_type = rng.choice(ABSENCE_TYPES_PLANNED, p=[0.70, 0.15, 0.15])

    return True, absence_type, is_unplanned
