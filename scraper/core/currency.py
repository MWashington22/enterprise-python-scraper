"""
Currency conversion module.

Responsible for:
- Fetching the GBP → USD exchange rate from an API
- Providing a fallback rate if the API fails
- Ensuring the scraper always has a usable conversion value
"""

import requests  # Used to make HTTP requests to the exchange rate API

# URL for the free exchange rate API
EXCHANGE_API_URL = "https://open.er-api.com/v6/latest/GBP"


def get_gbp_to_usd_rate(session, fallback: float = 1.24, proxies=None) -> float:
    """
    Retrieves the GBP → USD exchange rate.

    Parameters:
        session: shared requests.Session() with retry logic
        fallback: default rate used if the API call fails
        proxies: optional proxy configuration

    Returns:
        float: the exchange rate (GBP → USD)
    """

    try:
        # Make the API request using the shared session
        resp = session.get(EXCHANGE_API_URL, timeout=10, proxies=proxies)

        # Parse the JSON response into a Python dictionary
        data = resp.json()

        # Extract the USD rate from the "rates" object
        return float(data["rates"]["USD"])

    except Exception:
        # If anything goes wrong (network error, JSON error, missing key),
        # return the fallback rate instead of crashing the scraper.
        return fallback