"""
Product detail scraping module.

Responsible for:
- Scraping each product's detail page
- Extracting:
    - availability
    - description
    - USD price (converted)
- Running all product scrapes concurrently using ThreadPoolExecutor
"""

from typing import Dict, List, Optional  # Type hints
from concurrent.futures import ThreadPoolExecutor, as_completed  # Concurrency tools
from bs4 import BeautifulSoup  # HTML parsing

from scraper.config import MAX_WORKERS  # Number of threads to use


def _scrape_product_detail(session, meta: Dict, rate: float, logger, proxies=None) -> Optional[Dict]:
    """
    Scrapes a single product detail page.

    Parameters:
        session: shared HTTP session
        meta: metadata dictionary from catalog scraper
        rate: GBP → USD conversion rate
        logger: rotating logger
        proxies: optional proxy configuration

    Returns:
        Dict: enriched product data
        None: if scraping fails
    """

    try:
        # Fetch the product detail page
        resp = session.get(meta["url"], timeout=10, proxies=proxies)
        resp.encoding = "utf-8"

        # Parse HTML
        soup = BeautifulSoup(resp.text, "lxml")

        # Extract availability text
        avail_tag = soup.find("p", class_="instock availability")
        availability = avail_tag.text.strip() if avail_tag else "Unknown"

        # Extract description from meta tag
        desc_tag = soup.find("meta", attrs={"name": "description"})
        description = desc_tag["content"].strip() if desc_tag else "No description"
        description = " ".join(description.split())  # Normalize whitespace

        # Convert price to USD
        price_usd = round(meta["price_gbp"] * rate, 2)

        # Return enriched product data
        return {
            "Product Name": meta["name"],
            "Price (USD)": price_usd,
            "Rating": meta["rating"],
            "Availability": availability,
            "Description": description,
            "Product URL": meta["url"],
        }

    except Exception as e:
        # Log failure and return None
        logger.error(f"Failed to scrape product page {meta['url']}: {e}")
        return None


def scrape_products(session, products_meta: List[Dict], rate: float, logger, proxies=None) -> List[Dict]:
    """
    Scrapes all product detail pages concurrently.

    Parameters:
        session: shared HTTP session
        products_meta: list of metadata dictionaries
        rate: GBP → USD conversion rate
        logger: rotating logger
        proxies: optional proxy configuration

    Returns:
        List[Dict]: list of enriched product data
    """

    results = []  # Stores enriched product data

    logger.info(f"Scraping {len(products_meta)} product pages with {MAX_WORKERS} workers")

    # Create a thread pool for concurrent scraping
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

        # Submit each product detail scrape as a separate task
        futures = [
            executor.submit(_scrape_product_detail, session, meta, rate, logger, proxies)
            for meta in products_meta
        ]

        # Process completed tasks as they finish
        for future in as_completed(futures):
            res = future.result()
            if res:
                results.append(res)

    logger.info(f"Product details collected: {len(results)} items")
    return results