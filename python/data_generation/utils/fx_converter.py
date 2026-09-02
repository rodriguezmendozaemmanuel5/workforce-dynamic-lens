# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.6.0
# Foreign Exchange & Currency Conversion Utility
# =============================================================================

from typing import Dict, Any

class FXConverter:
    def __init__(self, fx_rates: Dict[str, Any]):
        self.fx_rates = fx_rates

    def convert_local_to_annual_usd(self, base_salary_orig: float, country_code: str) -> float:
        """Converts local monthly base salary to annualized USD."""
        country_info = self.fx_rates.get(country_code)
        if not country_info:
            raise ValueError(f"Unknown country_code: {country_code}")
        
        fx_rate = country_info["fx_rate_to_usd"]
        annual_mult = country_info["annual_multiplier"]
        
        annual_usd = (base_salary_orig * annual_mult) * fx_rate
        return round(annual_usd, 2)

    def calculate_fully_loaded_cost(self, annual_salary_usd: float) -> float:
        """Calculates fully loaded employee cost including 30% overhead (BR-17)."""
        return round(annual_salary_usd * 1.30, 2)
