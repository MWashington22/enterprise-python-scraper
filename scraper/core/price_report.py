from pathlib import Path

import pandas as pd


def generate_price_reports(logger):
    logger.info("Generating price comparison reports...")

    data_dir = Path(__file__).resolve().parents[1] / "data"

    history_file = data_dir / "price_history.csv"

    if not history_file.exists():
        logger.warning("Price history file not found.")
        return

    history = pd.read_csv(history_file)

    required_columns = [
        "scraped_at",
        "product_url",
        "product_name",
        "price_usd"
    ]

    for column in required_columns:
        if column not in history.columns:
            raise ValueError(f"Missing required column: {column}")

    history["scraped_at"] = pd.to_datetime(
        history["scraped_at"], utc=True
    )

    history["price_usd"] = pd.to_numeric(
        history["price_usd"], errors="coerce"
    )

    history = history.dropna(
        subset=["scraped_at", "product_url", "price_usd"]
    )

    snapshots = sorted(history["scraped_at"].unique())

    if len(snapshots) < 2:
        logger.warning("At least two snapshots are required.")
        return

    previous_time = snapshots[-2]
    current_time = snapshots[-1]

    previous = history[
        history["scraped_at"] == previous_time
    ].copy()

    current = history[
        history["scraped_at"] == current_time
    ].copy()

    # Match products using their URLs
    comparison = current.merge(
        previous[["product_url", "price_usd"]],
        on="product_url",
        how="inner",
        suffixes=("_current", "_previous")
    )

    comparison = comparison.rename(columns={
        "price_usd_current": "current_price",
        "price_usd_previous": "previous_price"
    })

    comparison["price_difference"] = (
        comparison["current_price"]
        - comparison["previous_price"]
    )

    comparison["percentage_change"] = (
        comparison["price_difference"]
        / comparison["previous_price"]
    ) * 100

    comparison["change_type"] = comparison[
        "price_difference"
    ].apply(
        lambda value:
            "Increase" if value > 0
            else "Decrease" if value < 0
            else "No Change"
    )

    comparison = comparison.rename(columns={
        "product_name": "Product Name",
        "product_url": "Product URL"
    })

    # Export all comparisons
    changed = comparison[
        comparison["price_difference"] != 0
    ].copy()

    changed = changed.sort_values(
        "percentage_change"
    )

    changed.to_csv(
        data_dir / "price_changes.csv",
        index=False
    )

    # Export price decreases
    drops = changed[
        changed["price_difference"] < 0
    ].copy()

    drops.to_csv(
        data_dir / "price_drops.csv",
        index=False
    )

    # Export price increases
    increases = changed[
        changed["price_difference"] > 0
    ].copy()

    increases.to_csv(
        data_dir / "price_increases.csv",
        index=False
    )

    # Export the ten largest percentage price drops
    top_drops = drops.nsmallest(
        10, "percentage_change"
    )

    top_drops.to_csv(
        data_dir / "top_price_drops.csv",
        index=False
    )

    logger.info(
        f"Products compared: {len(comparison)}"
    )

    logger.info(
        f"Price decreases: {len(drops)}"
    )

    logger.info(
        f"Price increases: {len(increases)}"
    )

    logger.info(
        f"Total price changes: {len(changed)}"
    )

    logger.info("Price reports generated successfully.")