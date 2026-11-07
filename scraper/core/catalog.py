"""
Catalog scraping module.

Responsible for:
- Looping through all catalog pages (1 → TOTAL_PAGES)
- Extracting product metadata:
    - name
    - price in GBP
    - rating (1–5)
    - product detail URL
- Handling retries for failed pages
- Returning a list of product metadata dictionaries
"""

import time  # Used for delays between requests
import re  # Used to clean price strings
from typing import List, Dict  # Type hints for clarity
from bs4 import BeautifulSoup  # HTML parsing library
from tqdm import tqdm  # Progress bar for catalog scraping

# Import configuration values
from scraper.config import BASE_URL, TOTAL_PAGES, RETRIES, DELAY, PRODUCT_BASE


def scrape_catalog(session, logger, proxies=None) -> List[Dict]:
    """
    Scrapes all catalog pages and extracts product metadata.

    Parameters:
        session: shared HTTP session
        logger: rotating logger instance
        proxies: optional proxy configuration

    Returns:
        List[Dict]: list of product metadata dictionaries
    """

    products_meta = []  # Stores metadata for all products

    logger.info(f"Scraping {TOTAL_PAGES} catalog pages")

    # Loop through each catalog page with a progress bar
    for page in tqdm(range(1, TOTAL_PAGES + 1), desc="Catalog pages", ncols=80):

        # Build the URL for the current page
        url = BASE_URL.format(page)

        success = False  # Tracks whether the page was successfully scraped

        # Retry loop for handling temporary failures
        for attempt in range(RETRIES):
            try:
                # Fetch the page HTML
                resp = session.get(url, timeout=10, proxies=proxies)
                resp.encoding = "utf-8"  # Ensure correct text encoding

                # Parse the HTML using lxml parser (fast + robust)
                soup = BeautifulSoup(resp.text, "lxml")

                # Find all product cards on the page
                items = soup.find_all("article", class_="product_pod")

                # Extract metadata from each product card
                for item in items:
                    name = item.h3.a["title"].strip()  # Product name

                    # Extract price and convert to float
                    price_gbp = float(
                        re.sub(r"[^\d.]", "", item.find("p", class_="price_color").text)
                    )

                    # Extract rating from CSS class
                    rating_text = item.find("p", class_="star-rating")["class"][1]
                    rating_dict = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
                    rating = rating_dict.get(rating_text, 0)

                    # Build full product detail URL
                    product_url = PRODUCT_BASE + item.h3.a["href"]

                    # Store metadata in a dictionary
                    products_meta.append({
                        "name": name,
                        "price_gbp": price_gbp,
                        "rating": rating,
                        "url": product_url,
                    })

                success = True  # Mark page as successfully scraped
                break  # Exit retry loop

            except Exception as e:
                # Log the failure and retry
                logger.warning(f"Retry {attempt+1} failed for page {page}: {e}")
                time.sleep(1)  # Wait before retrying

        if not success:
            # Log a final error if all retries failed
            logger.error(f"Failed to fetch page {page} after {RETRIES} retries")

        # Delay between pages to avoid overwhelming the server
        time.sleep(DELAY)

    logger.info(f"Catalog metadata collected: {len(products_meta)} items")
    return products_meta