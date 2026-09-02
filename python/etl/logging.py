# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.6.0
# ETL Layer: ETL Audit Logging (etl_load_history)
# =============================================================================

from datetime import datetime
from sqlalchemy import text
from sqlalchemy.engine import Engine
from python.data_generation.utils.logger import setup_logger

logger = setup_logger("etl.logging")


def log_start(engine: Engine, target_table: str, source_file: str,
              source_system: str = "synthetic_generator",
              checksum: str = None) -> int:
    """
    Inserts a new ETL run record with status RUNNING.
    Returns the load_id for subsequent updates.
    """
    with engine.begin() as conn:
        result = conn.execute(text("""
            INSERT INTO people_analytics.etl_load_history
                (target_table, source_system, status, source_file, checksum, load_start_ts)
            VALUES
                (:table, :system, 'RUNNING', :file, :checksum, NOW())
            RETURNING load_id
        """), {
            "table": target_table,
            "system": source_system,
            "file": source_file,
            "checksum": checksum
        })
        load_id = result.scalar()
    logger.info(f"[{target_table}] ETL run started — load_id={load_id}")
    return load_id


def log_success(engine: Engine, load_id: int, rows_inserted: int,
                rows_updated: int = 0, rows_rejected: int = 0) -> None:
    """Marks an ETL run as SUCCESS with final row counts."""
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE people_analytics.etl_load_history
            SET status        = 'SUCCESS',
                rows_inserted = :inserted,
                rows_updated  = :updated,
                rows_rejected = :rejected,
                load_end_ts   = NOW()
            WHERE load_id = :load_id
        """), {
            "load_id": load_id,
            "inserted": rows_inserted,
            "updated": rows_updated,
            "rejected": rows_rejected
        })
    logger.info(f"[load_id={load_id}] ETL run SUCCESS — inserted={rows_inserted}, rejected={rows_rejected}")


def log_failure(engine: Engine, load_id: int, error_message: str) -> None:
    """Marks an ETL run as FAILED with the exception message."""
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE people_analytics.etl_load_history
            SET status        = 'FAILED',
                error_message = :error,
                load_end_ts   = NOW()
            WHERE load_id = :load_id
        """), {"load_id": load_id, "error": error_message[:2000]})
    logger.error(f"[load_id={load_id}] ETL run FAILED — {error_message[:200]}")


def already_loaded(engine: Engine, target_table: str, checksum: str) -> bool:
    """
    Idempotency guard: returns True if a SUCCESS run with the same
    checksum already exists. Prevents re-loading unchanged files.
    """
    if checksum is None:
        return False
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT COUNT(*) FROM people_analytics.etl_load_history
            WHERE target_table = :table
              AND checksum      = :checksum
              AND status        = 'SUCCESS'
        """), {"table": target_table, "checksum": checksum}).scalar()
    if result > 0:
        logger.info(f"[{target_table}] Skipping — identical checksum already loaded successfully.")
        return True
    return False
