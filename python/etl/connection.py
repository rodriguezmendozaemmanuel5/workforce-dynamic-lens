# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.6.0
# ETL Layer: Database Connection & Engine Management
# =============================================================================

import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from python.data_generation.utils.logger import setup_logger

logger = setup_logger("etl.connection")

DEFAULT_DB_URL = (
    "postgresql+psycopg2://workforce_admin:workforce_pass@localhost:5432/workforce_db"
)


def get_engine(db_url: str = None) -> Engine:
    """
    Creates and returns a SQLAlchemy Engine for PostgreSQL.
    Reads DB_URL from environment if not explicitly provided.
    Connection pooling configured for ETL bulk-load patterns.
    """
    url = db_url or os.environ.get("WDL_DB_URL", DEFAULT_DB_URL)
    engine = create_engine(
        url,
        connect_args={"client_encoding": "utf8"},
        pool_pre_ping=True,       # Detect stale connections before using them
        pool_size=5,
        max_overflow=2,
        echo=False
    )
    return engine


def test_connection(engine: Engine) -> bool:
    """Verifies connectivity and schema existence before pipeline execution."""
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'people_analytics'")
            ).fetchone()
            if result:
                logger.info("[PASS] PostgreSQL connection established. Schema 'people_analytics' found.")
                return True
            else:
                logger.error("[FAIL] Schema 'people_analytics' not found. Run sql/schema/01_database_schema.sql first.")
                return False
    except Exception as e:
        logger.error(f"[FAIL] Cannot connect to PostgreSQL: {e}")
        return False
