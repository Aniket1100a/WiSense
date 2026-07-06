import logging
import sys
from logging.config import dictConfig


def configure_logging(debug: bool = False) -> None:
    """Configure structured logging for the application."""

    level = logging.DEBUG if debug else logging.INFO

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s %(levelname)s [%(name)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "standard",
            }
        },
        "root": {
            "handlers": ["default"],
            "level": level,
        },
        "loggers": {
            "uvicorn.error": {
                "level": level,
                "handlers": ["default"],
                "propagate": False,
            },
            "uvicorn.access": {
                "level": level,
                "handlers": ["default"],
                "propagate": False,
            },
        },
    }

    dictConfig(logging_config)
