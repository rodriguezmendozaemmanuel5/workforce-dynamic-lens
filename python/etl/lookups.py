# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.7.0
# ETL Layer: NK → SK Lookup Dictionary Builders
# =============================================================================

from typing import Dict
from sqlalchemy import text
from sqlalchemy.engine import Engine
from python.data_generation.utils.logger import setup_logger

logger = setup_logger("etl.lookups")


def build_department_lookup(engine: Engine) -> Dict[str, int]:
    """
    Returns {department_id (NK) → department_sk (SK)} for all departments.
    Called after load_departments() so SKs are guaranteed to exist.
    """
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT department_id, department_sk FROM people_analytics.dim_departments"
        )).fetchall()
    lookup = {r.department_id: r.department_sk for r in rows}
    logger.info(f"[lookup] dim_departments: {len(lookup)} NK→SK mappings built.")
    return lookup


def build_position_lookup(engine: Engine) -> Dict[str, int]:
    """Returns {position_id → position_sk}."""
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT position_id, position_sk FROM people_analytics.dim_positions"
        )).fetchall()
    lookup = {r.position_id: r.position_sk for r in rows}
    logger.info(f"[lookup] dim_positions: {len(lookup)} NK→SK mappings built.")
    return lookup


def build_employee_lookup(engine: Engine) -> Dict[str, int]:
    """
    Returns {employee_id → employee_sk} for CURRENT rows only.
    Fact tables reference the current employee version (is_current_row=TRUE),
    encompassing both active employees and terminated employees.
    """
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT employee_id, employee_sk
            FROM people_analytics.dim_employees
            WHERE is_current_row = TRUE
        """)).fetchall()
    lookup = {r.employee_id: r.employee_sk for r in rows}
    logger.info(f"[lookup] dim_employees (current rows): {len(lookup)} NK→SK mappings built.")
    return lookup


def build_date_lookup(engine: Engine) -> Dict[str, int]:
    """
    Returns {date_actual (YYYY-MM-DD string) → date_sk (YYYYMMDD integer)}.
    dim_date uses its own surrogate (YYYYMMDD integer) not IDENTITY,
    so the lookup is deterministic without a DB query —
    but we still read from DB to confirm population.
    """
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT date_actual::TEXT, date_sk FROM people_analytics.dim_date"
        )).fetchall()
    lookup = {r.date_actual: r.date_sk for r in rows}
    logger.info(f"[lookup] dim_date: {len(lookup)} date→date_sk mappings built.")
    return lookup
