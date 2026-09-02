# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.6.0
# Structured Logging Utility
# =============================================================================

import logging
import os
from pathlib import Path

def setup_logger(name: str = "workforce_generator", log_dir: str = "logs") -> logging.Logger:
    """Configures structured logger with console and file handlers."""
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_file = Path(log_dir) / "generation.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
        )

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
