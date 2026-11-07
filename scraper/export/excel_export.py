"""
Excel export module.

Responsible for:
- Writing the final DataFrame to an Excel (.xlsx) file
- Logging success or failure
"""

from scraper.config import OUTPUT_FILES


def export_excel(df, logger):
    """
    Exports the DataFrame to an Excel file.
    """

    df.to_excel(OUTPUT_FILES["excel"], index=False)
    # ^ Write DataFrame to Excel

    logger.info(f"Excel exported to {OUTPUT_FILES['excel']}")
    # ^ Log successful export