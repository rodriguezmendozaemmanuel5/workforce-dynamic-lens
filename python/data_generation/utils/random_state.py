# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.6.0
# Global Reproducibility & Random State Manager
# =============================================================================

import numpy as np
import random

class SeedManager:
    _rng: np.random.Generator = None
    _seed: int = 42

    @classmethod
    def set_seed(cls, seed: int = 42) -> np.random.Generator:
        """Sets fixed seed across numpy and Python random module for 100% reproducibility."""
        cls._seed = seed
        random.seed(seed)
        cls._rng = np.random.default_rng(seed)
        return cls._rng

    @classmethod
    def get_rng(cls) -> np.random.Generator:
        """Returns the initialized numpy random Generator instance."""
        if cls._rng is None:
            return cls.set_seed(42)
        return cls._rng
