"""
Logging utilities for the enterprise scraper.
Provides a rotating log handler with consistent formatting.
"""

import logging  # Python's built-in logging framework
from logging.handlers import RotatingFileHandler  # Enables rotating log files
from pathlib import Path  # For OS-safe file paths

# -----------------------------
# Log directory setup
# -----------------------------

LOG_DIR = Path("scraper/logs")  
# ^ Directory where log files will be stored

LOG_DIR.mkdir(exist_ok=True, parents=True)  
# ^ Creates the logs directory if it doesn't already exist

# -----------------------------
# Logger factory function
# -----------------------------

def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a configured logger instance.
    Ensures consistent formatting and rotating log behavior.
    """

    logger = logging.getLogger(name)  
    # ^ Retrieves (or creates) a logger with the given name

    logger.setLevel(logging.INFO)  
    # ^ Sets the minimum log level (INFO and above will be logged)

    # Prevent duplicate handlers if logger is created multiple times
    if not logger.handlers:

        handler = RotatingFileHandler(
            LOG_DIR / "scraper.log",  # Log file path
            maxBytes=1_000_000,       # Rotate after ~1MB
            backupCount=5             # Keep up to 5 old log files
        )

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        # ^ Defines the log message format (timestamp, logger name, level, message)

        handler.setFormatter(formatter)  
        # ^ Applies the formatter to the handler

        logger.addHandler(handler)  
        # ^ Attaches the handler to the logger

    return logger  
    # ^ Returns the fully configured logger