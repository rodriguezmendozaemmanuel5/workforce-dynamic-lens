# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.6.0
# Entity Generator 04: Employee Dimension (dim_employees — SCD Type 2)
# =============================================================================

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple, List, Dict, Any

from python.data_generation.utils.config_loader import ConfigLoader
from python.data_generation.utils.random_state import SeedManager
from python.data_generation.utils.fx_converter import FXConverter
from python.data_generation.utils.logger import setup_logger

from python.data_generation.distributions.tenure_distribution import generate_hire_date
from python.data_generation.distributions.salary_distribution import generate_salary_around_midpoint
from python.data_generation.distributions.performance_distribution import generate_performance_and_potential

logger = setup_logger("employee_generator")

FIRST_NAMES = {
    "MEX": ["Carlos", "Sofia", "Alejandro", "Valeria", "Mateo", "Camila", "Diego", "Lucia", "Javier", "Fernanda"],
    "COL": ["Andres", "Mariana", "Santiago", "Daniela", "Sebastian", "Valentina", "Nicolas", "Gabriela", "Felipe", "Isabella"],
    "BRA": ["Gabriel", "Beatriz", "Lucas", "Mariana", "Rodrigo", "Juliana", "Felipe", "Larissa", "Thiago", "Camila"],
    "ESP": ["Pablo", "Carmen", "Gonzalo", "Lucia", "Hugo", "Paula", "Adrian", "Alba", "Marcos", "Elena"],
    "DEU": ["Maximilian", "Sophie", "Alexander", "Hannah", "Lukas", "Emma", "Felix", "Mia", "Leon", "Anna"]
}

LAST_NAMES = {
    "MEX": ["Hernandez", "Garcia", "Martinez", "Lopez", "Gonzalez", "Perez", "Rodriguez", "Sanchez"],
    "COL": ["Rodriguez", "Gomez", "Lopez", "Gonzalez", "Garcia", "Martinez", "Diaz", "Perez"],
    "BRA": ["Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira"],
    "ESP": ["Garcia", "Rodriguez", "Gonzalez", "Fernandez", "Lopez", "Martinez", "Sanchez", "Perez"],
    "DEU": ["Muller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker"]
}

def generate_employees(config_loader: ConfigLoader = None,
                       depts_df: pd.DataFrame = None,
                       pos_df: pd.DataFrame = None,
                       benchmarks_df: pd.DataFrame = None) -> pd.DataFrame:
    """Generates dim_employees DataFrame including SCD Type 2 historical records."""
    if config_loader is None:
        config_loader = ConfigLoader()
    
    config = config_loader.load_yaml_config()
    fx_rates = config_loader.load_fx_rates()
    converter = FXConverter(fx_rates)
    rng = SeedManager.get_rng()

    target_count = config["company_scale"].get("historical_employee_population", config["company_scale"].get("target_active_headcount", 4500))
    scd2_ratio = config["company_scale"]["scd2_history_percentage"]
    countries = config["countries"]

    dept_ids = depts_df["department_id"].tolist() if depts_df is not None else ["DEP_ENG", "DEP_RD", "DEP_CLINICAL"]
    pos_ids = pos_df["position_id"].tolist() if pos_df is not None else ["POS_ENG_SR", "POS_ENG_JR"]

    # Map benchmarks midpoint lookup: (position_id, country_code) -> midpoint_usd
    bmk_lookup = {}
    if benchmarks_df is not None:
        for _, b_row in benchmarks_df.iterrows():
            bmk_lookup[(b_row["position_id"], b_row["country_code"])] = b_row["market_midpoint_salary_usd"]

    country_codes = [c["code"] for c in countries]
    country_probs = [c["weight"] for c in countries]

    rows = []
    
    for i in range(1, target_count + 1):
        emp_id = f"EMP{i:05d}"
        country = rng.choice(country_codes, p=country_probs)
        gender = rng.choice(["Masculino", "Femenino", "No Binario"], p=[0.49, 0.49, 0.02])
        
        first_name = rng.choice(FIRST_NAMES.get(country, ["Alex"]))
        last_name = rng.choice(LAST_NAMES.get(country, ["Smith"]))
        email = f"{first_name.lower()}.{last_name.lower()}{i}@medtech.com"

        hire_dt = generate_hire_date(start_year=2012)
        tenure_months = (datetime(2025, 12, 31) - hire_dt).days / 30.4375

        # Sample birth date (age 22 to 62 at hire)
        age_at_hire = rng.uniform(22, 50)
        birth_dt = hire_dt - timedelta(days=int(age_at_hire * 365.25))

        dept_id = rng.choice(dept_ids)
        pos_id = rng.choice(pos_ids)
        work_loc = rng.choice(["Presencial", "Híbrido", "Remoto"], p=[0.40, 0.45, 0.15])

        # Get salary benchmark or default
        midpoint_usd = bmk_lookup.get((pos_id, country), 45000.00)
        annual_usd = generate_salary_around_midpoint(midpoint_usd, scarcity_index=1.8)
        
        # Local base salary
        fx_rate = fx_rates[country]["fx_rate_to_usd"]
        mult = fx_rates[country]["annual_multiplier"]
        base_orig = round((annual_usd / mult) / fx_rate, 2)
        curr_orig = fx_rates[country]["currency_code"]
        fully_loaded = converter.calculate_fully_loaded_cost(annual_usd)

        perf_rating, potential_rating = generate_performance_and_potential(tenure_months)

        # Decide if employee has SCD2 history (15% probability)
        has_scd2_history = rng.random() < scd2_ratio and tenure_months >= 24.0

        if has_scd2_history:
            # Historical Row (Old position/dept/salary) — R09: historical rows were active during their period
            change_date = hire_dt + timedelta(days=int((datetime(2025, 12, 31) - hire_dt).days * 0.5))
            prev_annual_usd = round(annual_usd * 0.85, 2)
            prev_base_orig = round((prev_annual_usd / mult) / fx_rate, 2)

            rows.append({
                "employee_id": emp_id,
                "first_name": first_name,
                "last_name": last_name,
                "work_email": email,
                "gender": gender,
                "birth_date": birth_dt.strftime("%Y-%m-%d"),
                "hire_date": hire_dt.strftime("%Y-%m-%d"),
                "department_id": rng.choice(dept_ids),
                "position_id": rng.choice(pos_ids),
                "country_code": country,
                "work_location_type": work_loc,
                "base_salary_orig": prev_base_orig,
                "salary_currency_orig": curr_orig,
                "annual_base_salary_usd": prev_annual_usd,
                "fully_loaded_cost_usd": converter.calculate_fully_loaded_cost(prev_annual_usd),
                "performance_rating": perf_rating,
                "potential_rating": potential_rating,
                "is_active": True,
                "is_current_row": False,
                "row_effective_date": hire_dt.strftime("%Y-%m-%d"),
                "row_expiration_date": (change_date - timedelta(days=1)).strftime("%Y-%m-%d")
            })

            # Current Row
            rows.append({
                "employee_id": emp_id,
                "first_name": first_name,
                "last_name": last_name,
                "work_email": email,
                "gender": gender,
                "birth_date": birth_dt.strftime("%Y-%m-%d"),
                "hire_date": hire_dt.strftime("%Y-%m-%d"),
                "department_id": dept_id,
                "position_id": pos_id,
                "country_code": country,
                "work_location_type": work_loc,
                "base_salary_orig": base_orig,
                "salary_currency_orig": curr_orig,
                "annual_base_salary_usd": annual_usd,
                "fully_loaded_cost_usd": fully_loaded,
                "performance_rating": perf_rating,
                "potential_rating": potential_rating,
                "is_active": True,
                "is_current_row": True,
                "row_effective_date": change_date.strftime("%Y-%m-%d"),
                "row_expiration_date": "9999-12-31"
            })
        else:
            # Single Current Row
            rows.append({
                "employee_id": emp_id,
                "first_name": first_name,
                "last_name": last_name,
                "work_email": email,
                "gender": gender,
                "birth_date": birth_dt.strftime("%Y-%m-%d"),
                "hire_date": hire_dt.strftime("%Y-%m-%d"),
                "department_id": dept_id,
                "position_id": pos_id,
                "country_code": country,
                "work_location_type": work_loc,
                "base_salary_orig": base_orig,
                "salary_currency_orig": curr_orig,
                "annual_base_salary_usd": annual_usd,
                "fully_loaded_cost_usd": fully_loaded,
                "performance_rating": perf_rating,
                "potential_rating": potential_rating,
                "is_active": True,
                "is_current_row": True,
                "row_effective_date": hire_dt.strftime("%Y-%m-%d"),
                "row_expiration_date": "9999-12-31"
            })

    df = pd.DataFrame(rows)
    logger.info(f"Generated dim_employees dataset: {len(df)} rows ({target_count} total employees generated).")
    return df
