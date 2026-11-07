"""
JSON export module.

Responsible for:
- Writing the final DataFrame to a JSON file
- Logging success or failure
"""

from scraper.config import OUTPUT_FILES


def export_json(df, logger):
    """
    Exports the DataFrame to a JSON file.
    """

    df.to_json(OUTPUT_FILES["json"], orient="records", indent=4)
    # ^ Convert DataFrame to JSON array of objects

    logger.info(f"JSON exported to {OUTPUT_FILES['json']}")
    # ^ Log successful export