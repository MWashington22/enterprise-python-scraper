import pandas as pd
from tqdm import tqdm

# Import scraping functions
from scraper.core.catalog import scrape_catalog
from scraper.core.product import scrape_products
from scraper.core.validation import validate_dataframe
from scraper.core.price_tracker import track_prices
from scraper.core.price_report import generate_price_reports
from scraper.core.email_alerts import send_price_alerts


def run_pipeline(session, rate, logger, exporters, proxies=None):

    tqdm.write("Starting pipeline...")

    # 1. Catalog scraping
    tqdm.write("Scraping catalog pages...")

    products = scrape_catalog(
        session,
        logger,
        proxies=proxies
    )

    tqdm.write(
        f"Catalog scrape complete. Items found: {len(products)}"
    )

    if not products:
        logger.warning("No products found. Pipeline stopped.")
        return

    # 2. Product detail scraping
    tqdm.write("Scraping product details...")

    details = scrape_products(
        session,
        products,
        rate,
        logger,
        proxies=proxies
    )

    tqdm.write(
        f"Detail scrape complete. Records processed: {len(details)}"
    )

    if not details:
        logger.warning("No product details collected.")
        return

    # 3. Build DataFrame
    tqdm.write("Building final DataFrame...")

    final_df = pd.DataFrame(details)

    tqdm.write(f"Final dataset size: {len(final_df)} rows")

    # Validate product data
    tqdm.write("Validating product data...")

    final_df = validate_dataframe(final_df, logger)

    tqdm.write(
        f"Validated dataset size: {len(final_df)} rows"
    )

    tqdm.write("Tracking historical prices...")
    track_prices(final_df, logger)
    tqdm.write("Price tracking completed.")

    tqdm.write("Generating price reports...")
    generate_price_reports(logger)
    tqdm.write("Price reports generated.")

    tqdm.write("Checking for price alerts...")
    send_price_alerts(logger)
    tqdm.write("Email alert check completed.")

    # 4. Export data
    tqdm.write("Exporting data...")

    for exporter in exporters:
        try:
            exporter(final_df, logger)

        except Exception as e:
            logger.exception(
                f"Export failed using {exporter.__name__}: {e}"
            )

    tqdm.write("Pipeline finished.")