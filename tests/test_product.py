from unittest.mock import MagicMock

from scraper.core.product import _scrape_product_detail
from scraper.core.product import scrape_products


def create_test_meta():
    return {
        "name": "Test Product",
        "price_gbp": 10.00,
        "rating": 5,
        "url": "https://example.com/product1"
    }


def create_mock_session(html):
    session = MagicMock()
    response = MagicMock()

    response.text = html

    session.get.return_value = response

    return session


def test_product_details_are_extracted():
    html = """
    <html>
        <body>
            <p class="instock availability">
                In stock (20 available)
            </p>
            <meta name="description"
                  content="A great test product">
        </body>
    </html>
    """

    session = create_mock_session(html)
    meta = create_test_meta()
    logger = MagicMock()

    result = _scrape_product_detail(
        session, meta, 1.35, logger
    )

    assert result["Product Name"] == "Test Product"
    assert result["Price (USD)"] == 13.50
    assert result["Rating"] == 5
    assert result["Availability"] == "In stock (20 available)"
    assert result["Description"] == "A great test product"
    assert result["Product URL"] == meta["url"]


def test_missing_html_elements_use_defaults():
    session = create_mock_session("<html><body></body></html>")
    meta = create_test_meta()
    logger = MagicMock()

    result = _scrape_product_detail(
        session, meta, 1.35, logger
    )

    assert result["Availability"] == "Unknown"
    assert result["Description"] == "No description"


def test_description_whitespace_is_normalized():
    html = """
    <html>
        <meta name="description"
              content="  This   is
              a   test   description  ">
    </html>
    """

    session = create_mock_session(html)
    meta = create_test_meta()
    logger = MagicMock()

    result = _scrape_product_detail(
        session, meta, 1.35, logger
    )

    assert result["Description"] == "This is a test description"


def test_failed_request_returns_none():
    session = MagicMock()

    session.get.side_effect = Exception("Connection failed")

    meta = create_test_meta()
    logger = MagicMock()

    result = _scrape_product_detail(
        session, meta, 1.35, logger
    )

    assert result is None
    logger.error.assert_called_once()

def test_scrape_products_collects_successful_results(monkeypatch):
    import scraper.core.product as product_module

    def mock_scrape(session, meta, rate, logger, proxies=None):
        if meta["name"] == "Failed Product":
            return None

        return {"Product Name": meta["name"]}

    monkeypatch.setattr(
        product_module,
        "_scrape_product_detail",
        mock_scrape
    )

    products = [
        {"name": "Product A"},
        {"name": "Failed Product"},
        {"name": "Product B"}
    ]

    logger = MagicMock()

    results = scrape_products(
        None, products, 1.35, logger
    )

    assert len(results) == 2

    names = [product["Product Name"] for product in results]

    assert "Product A" in names
    assert "Product B" in names
    assert "Failed Product" not in names


def test_scrape_products_handles_empty_list():
    logger = MagicMock()

    results = scrape_products(
        None, [], 1.35, logger
    )

    assert results == []