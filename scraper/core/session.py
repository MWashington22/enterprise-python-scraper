"""
HTTP session factory with retry strategy.
Ensures consistent, resilient networking across the scraper.
"""

import requests  # HTTP client library
from requests.adapters import HTTPAdapter  # Allows mounting retry-enabled adapters
from urllib3.util.retry import Retry  # Provides retry logic for failed requests

# -----------------------------
# Session factory function
# -----------------------------

def create_session() -> requests.Session:
    """
    Creates a requests.Session() configured with:
    - Retry strategy
    - Backoff behavior
    - HTTP/HTTPS adapters
    """

    session = requests.Session()  
    # ^ Creates a persistent HTTP session (faster + shared cookies)

    # -----------------------------
    # Retry strategy configuration
    # -----------------------------

    retry_strategy = Retry(
        total=5,                # Maximum number of retry attempts
        backoff_factor=1,       # Exponential backoff (1s, 2s, 4s...)
        status_forcelist=[429, 500, 502, 503, 504],  
        # ^ Retry only on these HTTP status codes

        allowed_methods=["GET"],  
        # ^ Only retry GET requests (safe, idempotent)
    )

    # -----------------------------
    # Adapter mounting
    # -----------------------------

    adapter = HTTPAdapter(max_retries=retry_strategy)  
    # ^ Wraps retry logic into an HTTP adapter

    session.mount("http://", adapter)  
    # ^ Applies retry logic to all HTTP requests

    session.mount("https://", adapter)  
    # ^ Applies retry logic to all HTTPS requests

    return session  
    # ^ Returns the fully configured session