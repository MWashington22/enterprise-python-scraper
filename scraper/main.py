"""
Main entrypoint for the enterprise scraper.

Responsible for:
- Initializing logging
- Creating the HTTP session
- Running the scraping pipeline
- Scheduling daily automated runs
"""

import time  # Used for scheduling loop
import schedule  # Lightweight task scheduler

# Import configuration and core modules
from scraper.config import PROXIES
from scraper.core.session import create_session
from scraper.core.pipeline import run_pipeline
from scraper.core.currency import get_gbp_to_usd_rate
from scraper.utils.logger import get_logger

# Import export modules
from scraper.export.csv_export import export_csv
from scraper.export.excel_export import export_excel
from scraper.export.json_export import export_json
from scraper.export.postgres_export import export_postgres


import logging
from tqdm import tqdm

class TqdmLoggingHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        tqdm.write(msg)

def get_logger():
    logger = logging.getLogger("pipeline")
    logger.setLevel(logging.INFO)

    handler = TqdmLoggingHandler()
    formatter = logging.Formatter("[%(asctime)s] %(message)s", "%H:%M:%S")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


def job():
    """
    Executes a single scraping run.
    """

    logger = get_logger()  # Create logger
    session = create_session()      # Create HTTP session

    # List of exporters to run after scraping
    exporters = [
        export_csv,
        export_excel,
        export_json,
        #export_postgres, # Uncomment if you want to export to PostgreSQL
    ]

    logger.info("Scraper job started")

    # Run the full scraping pipeline
    rate = get_gbp_to_usd_rate(session, proxies=PROXIES)

    logger.info(f"Using GBP to USD exchange rate: {rate}")

    run_pipeline(session, rate, logger, exporters, proxies=PROXIES)


if __name__ == "__main__":
    job()  # Run immediately when script is executed

    # Schedule daily run at 2:00 AM
    #schedule.every().day.at("02:00").do(job)

    #print("Automation system running. Waiting for scheduled tasks...")

    # Keep the scheduler running indefinitely
    #while True:
    #    schedule.run_pending()
    #    time.sleep(60)