"""Logging setup for CreditSetu AI backend."""

import logging
from logging.handlers import RotatingFileHandler

from backend.config import APP_LOG_PATH, LOGS_DIR


LOGGER_NAME = "creditsetu"


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a configured application logger."""
    LOGS_DIR.mkdir(exist_ok=True)
    logger = logging.getLogger(name or LOGGER_NAME)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    file_handler = RotatingFileHandler(
        APP_LOG_PATH,
        maxBytes=1_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
