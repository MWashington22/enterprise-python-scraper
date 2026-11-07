from pathlib import Path
from datetime import datetime, timezone

import pandas as pd


def track_prices(df, logger):
    logger.info("Starting historical price tracking...")

    data_dir = Path(__file__).resolve().parents[1] / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    history_file = data_dir / "price_history.csv"

    timestamp = datetime.now(timezone.utc).isoformat()

    # Create a consistent historical snapshot
    current = pd.DataFrame({
        "scraped_at": timestamp,
        "product_url": df["Product URL"],
        "product_name": df["Product Name"],
        "price_usd": pd.to_numeric(
            df["Price (USD)"], errors="coerce"
        )
    })

    if history_file.exists():
        history = pd.read_csv(history_file)

        previous = (
            history.sort_values("scraped_at")
            .drop_duplicates(
                subset="product_url",
                keep="last"
            )
        )

        previous_prices = previous.set_index(
            "product_url"
        )["price_usd"]

        current_previous = current["product_url"].map(
            previous_prices
        )

        changes = current[
            current_previous.notna()
            & (
                current["price_usd"].values
                != current_previous.values
            )
        ]

        logger.info(
            f"Price changes detected: {len(changes)}"
        )

    else:
        logger.info(
            "No historical data found. Starting first snapshot."
        )

    # Always append the same four columns
    current.to_csv(
        history_file,
        mode="a",
        header=not history_file.exists(),
        index=False
    )

    logger.info(f"Price history updated: {history_file}")

    return current