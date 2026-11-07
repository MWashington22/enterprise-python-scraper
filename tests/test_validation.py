import logging
import pandas as pd
import pytest

from scraper.core.validation import validate_dataframe


def create_test_data():
    return pd.DataFrame({
        "Product Name": ["Test Product", "Another Product"],
        "Price (USD)": [19.99, 29.99],
        "Rating": [5, 4],
        "Availability": ["In stock", "In stock"],
        "Description": ["Test description", "Another description"],
        "Product URL": [
            "https://example.com/product1",
            "https://example.com/product2"
        ]
    })


def test_valid_products_pass_validation():
    df = create_test_data()
    logger = logging.getLogger("test")

    result = validate_dataframe(df, logger)

    assert len(result) == 2
    assert result["Product Name"].notna().all()


def test_text_fields_are_trimmed():
    df = create_test_data()

    df.loc[0, "Product Name"] = "  Test Product  "
    df.loc[0, "Availability"] = "  In stock  "

    logger = logging.getLogger("test")

    result = validate_dataframe(df, logger)

    assert result.iloc[0]["Product Name"] == "Test Product"
    assert result.iloc[0]["Availability"] == "In stock"


def test_invalid_products_are_removed(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    (tmp_path / "scraper" / "data").mkdir(parents=True)

    df = create_test_data()

    df.loc[1, "Price (USD)"] = 0

    df.loc[0, "Product URL"] = "https://example.com/product1"
    df.loc[1, "Product URL"] = "https://example.com/product1"

    logger = logging.getLogger("test")

    result = validate_dataframe(df, logger)

    assert len(result) == 1

    report = tmp_path / "scraper" / "data" / "validation_issues.csv"

    assert report.exists()


def test_missing_required_column_raises_error():
    df = create_test_data()

    df = df.drop(columns=["Price (USD)"])

    logger = logging.getLogger("test")

    with pytest.raises(ValueError, match="Missing required column"):
        validate_dataframe(df, logger)

def test_invalid_prices_are_removed(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "scraper" / "data").mkdir(parents=True)

    df = create_test_data()

    df.loc[0, "Price (USD)"] = 0
    df.loc[1, "Price (USD)"] = -10

    logger = logging.getLogger("test")

    result = validate_dataframe(df, logger)

    assert len(result) == 0

def test_invalid_ratings_are_removed(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "scraper" / "data").mkdir(parents=True)

    df = create_test_data()

    df.loc[0, "Rating"] = 0
    df.loc[1, "Rating"] = 6

    logger = logging.getLogger("test")

    result = validate_dataframe(df, logger)

    assert len(result) == 0

def test_invalid_urls_are_removed(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "scraper" / "data").mkdir(parents=True)

    df = create_test_data()

    df.loc[0, "Product URL"] = "not-a-valid-url"

    logger = logging.getLogger("test")

    result = validate_dataframe(df, logger)

    assert len(result) == 1
    assert result.iloc[0]["Product URL"] == "https://example.com/product2"

def test_missing_product_name_is_removed(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "scraper" / "data").mkdir(parents=True)

    df = create_test_data()
    df.loc[0, "Product Name"] = ""

    logger = logging.getLogger("test")
    result = validate_dataframe(df, logger)

    assert len(result) == 1
    assert result.iloc[0]["Product Name"] == "Another Product"

def test_missing_availability_is_removed(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "scraper" / "data").mkdir(parents=True)

    df = create_test_data()
    df.loc[0, "Availability"] = ""

    logger = logging.getLogger("test")
    result = validate_dataframe(df, logger)

    assert len(result) == 1
    assert result.iloc[0]["Availability"] == "In stock"

def test_duplicate_urls_are_removed(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "scraper" / "data").mkdir(parents=True)

    df = create_test_data()

    df.loc[1, "Product URL"] = df.loc[0, "Product URL"]

    logger = logging.getLogger("test")
    result = validate_dataframe(df, logger)

    assert len(result) == 1
    assert result.iloc[0]["Product Name"] == "Test Product"