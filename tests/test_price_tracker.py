import pandas as pd
from unittest.mock import MagicMock

import scraper.core.price_tracker as tracker


def create_test_dataframe():
    return pd.DataFrame({
        "Product Name": ["Test Book", "Another Book"],
        "Price (USD)": [15.00, 25.00],
        "Product URL": [
            "https://example.com/book1",
            "https://example.com/book2"
        ]
    })


def test_first_snapshot_creates_price_history(tmp_path, monkeypatch):
    fake_file = tmp_path / "scraper" / "core" / "price_tracker.py"
    monkeypatch.setattr(tracker, "__file__", str(fake_file))

    logger = MagicMock()
    df = create_test_dataframe()

    result = tracker.track_prices(df, logger)

    history_file = tmp_path / "scraper" / "data" / "price_history.csv"

    assert history_file.exists()
    assert len(result) == 2
    assert list(result.columns) == [
        "scraped_at",
        "product_url",
        "product_name",
        "price_usd"
    ]

    saved_history = pd.read_csv(history_file)
    assert len(saved_history) == 2

    logger.info.assert_any_call(
        "No historical data found. Starting first snapshot."
    )

def test_new_snapshot_appends_to_existing_history(tmp_path, monkeypatch):
    fake_file = tmp_path / "scraper" / "core" / "price_tracker.py"
    monkeypatch.setattr(tracker, "__file__", str(fake_file))

    logger = MagicMock()
    df = create_test_dataframe()

    tracker.track_prices(df, logger)
    tracker.track_prices(df, logger)

    history_file = tmp_path / "scraper" / "data" / "price_history.csv"
    saved_history = pd.read_csv(history_file)

    assert len(saved_history) == 4
    assert saved_history["product_url"].nunique() == 2

def test_price_changes_are_detected(tmp_path, monkeypatch):
    fake_file = tmp_path / "scraper" / "core" / "price_tracker.py"
    monkeypatch.setattr(tracker, "__file__", str(fake_file))

    logger = MagicMock()
    df = create_test_dataframe()

    # Save the initial snapshot.
    tracker.track_prices(df, logger)

    # Change the first product's price.
    df.loc[0, "Price (USD)"] = 12.00

    # Track prices again.
    tracker.track_prices(df, logger)

    logger.info.assert_any_call("Price changes detected: 1")

def test_invalid_prices_are_converted_to_nan(tmp_path, monkeypatch):
    fake_file = tmp_path / "scraper" / "core" / "price_tracker.py"
    monkeypatch.setattr(tracker, "__file__", str(fake_file))

    logger = MagicMock()
    df = create_test_dataframe()

    df["Price (USD)"] = df["Price (USD)"].astype(object)
    df.loc[0, "Price (USD)"] = "invalid"

    result = tracker.track_prices(df, logger)

    assert pd.isna(result.loc[0, "price_usd"])
    assert result.loc[1, "price_usd"] == 25.00

    history_file = tmp_path / "scraper" / "data" / "price_history.csv"
    saved_history = pd.read_csv(history_file)

    assert pd.isna(saved_history.loc[0, "price_usd"])