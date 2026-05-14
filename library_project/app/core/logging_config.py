# app/core/logging_config.py
import logging
import sys
from pathlib import Path

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure root logger with:
    - Console handler  (stdout)
    - File handler     (logs/app.log)
    """
    Path("logs").mkdir(exist_ok=True)

    level = getattr(logging, log_level.upper(), logging.INFO)

    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/app.log", encoding="utf-8"),
    ]

    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=handlers,
        force=True,          # override any existing root config
    )

    # Silence noisy third-party loggers
    logging.getLogger("passlib").setLevel(logging.ERROR)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


# Module-level logger for the whole app
logger = logging.getLogger("library_app")
