"""
Global configuration for the enterprise scraper.
This module centralizes all constants, paths, and environment-based settings.
"""

import os  # Used to read environment variables for secure configuration
from pathlib import Path  # Provides OS-safe path handling

# -----------------------------
# Base URLs for scraping
# -----------------------------

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"  
# ^ URL template for catalog pages, {} will be replaced with page number

PRODUCT_BASE = "https://books.toscrape.com/catalogue/"  
# ^ Base URL used to build full product detail URLs

# -----------------------------
# Scraper behavior settings
# -----------------------------

TOTAL_PAGES = 100  
# ^ Number of catalog pages to scrape

MAX_WORKERS = 10  
# ^ Number of threads used for concurrent product scraping

RETRIES = 3  
# ^ Number of retry attempts for failed catalog page requests

DELAY = 0.5  
# ^ Delay between page requests to avoid hammering the server

# -----------------------------
# Output directory and file paths
# -----------------------------

OUTPUT_DIR = Path("scraper/data")  
# ^ Directory where CSV, Excel, and JSON files will be saved

OUTPUT_DIR.mkdir(exist_ok=True, parents=True)  
# ^ Creates the directory if it doesn't exist (safe for repeated runs)

OUTPUT_FILES = {
    "csv": OUTPUT_DIR / "products.csv",     # Path to CSV output
    "excel": OUTPUT_DIR / "products.xlsx",  # Path to Excel output
    "json": OUTPUT_DIR / "products.json",   # Path to JSON output
}

# -----------------------------
# Proxy configuration
# -----------------------------

PROXIES = {
    "http": None,   # No proxy for HTTP requests
    "https": None,  # No proxy for HTTPS requests
}

# -----------------------------
# Database configuration
# -----------------------------

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),  
    # ^ Reads DB host from environment variable, defaults to localhost

    "database": os.getenv("DB_NAME", "scraper_db"),  
    # ^ Database name

    "user": os.getenv("DB_USER", "postgres"),  
    # ^ Database username

    "password": os.getenv("DB_PASSWORD", "password"),  
    # ^ Database password (should be overridden in production)
}