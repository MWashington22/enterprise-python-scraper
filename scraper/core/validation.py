import pandas as pd
from urllib.parse import urlparse


def validate_dataframe(df, logger):

    logger.info("Starting data validation...")

    df = df.copy()

    issues = []

    initial_count = len(df)

    # 1. Normalize text fields
    text_columns = [
        "Product Name",
        "Availability",
        "Description",
        "Product URL"
    ]

    for column in text_columns:
        if column in df.columns:
            df[column] = df[column].apply(
                lambda value: value.strip()
                if isinstance(value, str)
                else value
            )

    # 2. Check required columns
    required_columns = [
        "Product Name",
        "Price (USD)",
        "Rating",
        "Availability",
        "Product URL"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"Missing required column: {column}"
            )

    # 3. Validate prices
    df["Price (USD)"] = pd.to_numeric(
        df["Price (USD)"],
        errors="coerce"
    )

    invalid_prices = (
        df["Price (USD)"].isna() |
        (df["Price (USD)"] <= 0)
    )

    for index in df[invalid_prices].index:
        issues.append({
            "Row": index,
            "Issue": "Invalid product price"
        })

    # 4. Validate ratings
    df["Rating"] = pd.to_numeric(
        df["Rating"],
        errors="coerce"
    )

    invalid_ratings = (
        df["Rating"].isna() |
        ~df["Rating"].between(1, 5)
    )

    for index in df[invalid_ratings].index:
        issues.append({
            "Row": index,
            "Issue": "Invalid product rating"
        })

    # 5. Validate required text fields
    for column in [
        "Product Name",
        "Availability",
        "Product URL"
    ]:

        invalid = (
            df[column].isna() |
            df[column].astype("string").str.strip().eq("")
        )

        for index in df[invalid].index:
            issues.append({
                "Row": index,
                "Issue": f"Missing {column}"
            })

    # 6. Validate product URLs
    def valid_url(value):
        if not isinstance(value, str):
            return False

        parsed = urlparse(value)

        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
        )

    invalid_urls = ~df["Product URL"].apply(valid_url)

    for index in df[invalid_urls].index:
        issues.append({
            "Row": index,
            "Issue": "Invalid product URL"
        })

    # 7. Remove duplicate product URLs
    duplicate_urls = df["Product URL"].duplicated(
        keep="first"
    )

    for index in df[duplicate_urls].index:
        issues.append({
            "Row": index,
            "Issue": "Duplicate product URL"
        })

    # 8. Remove invalid records
    invalid_records = (
        invalid_prices |
        invalid_ratings |
        invalid_urls
    )

    for column in [
        "Product Name",
        "Availability",
        "Product URL"
    ]:
        invalid_records |= (
            df[column].isna() |
            df[column].astype("string").str.strip().eq("")
        )

    clean_df = df.loc[
        ~invalid_records & ~duplicate_urls
    ].copy()

    # 9. Save validation report
    issues_df = pd.DataFrame(issues)

    if not issues_df.empty:
        issues_df.to_csv(
            "scraper/data/validation_issues.csv",
            index=False
        )

    # 10. Log results
    logger.info(
        f"Validation completed. "
        f"Original records: {initial_count}"
    )

    logger.info(
        f"Valid records: {len(clean_df)}"
    )

    logger.info(
        f"Issues detected: {len(issues_df)}"
    )

    return clean_df