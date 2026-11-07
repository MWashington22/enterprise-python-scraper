"""
CSV export module.

Responsible for:
- Writing the final DataFrame to a CSV file
- Logging success or failure
"""

from scraper.config import OUTPUT_FILES  # Import output file paths


def export_csv(df, logger):
    """
    Exports the DataFrame to a CSV file.

    Parameters:
        df: pandas DataFrame containing product data
        logger: rotating logger instance
    """

    df.to_csv(OUTPUT_FILES["csv"], index=False)
    # ^ Write the DataFrame to CSV without row numbers

    logger.info(f"CSV exported to {OUTPUT_FILES['csv']}")
    # ^ Log successful export