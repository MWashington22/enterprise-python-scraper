from unittest.mock import MagicMock, patch

from scraper.core.catalog import scrape_catalog


def create_product_html(name, price, rating, url):
    return f"""
    <article class="product_pod">
        <h3>
            <a title="{name}" href="{url}">Product</a>
        </h3>
        <p class="price_color">£{price}</p>
        <p class="star-rating {rating}"></p>
    </article>
    """


def create_mock_response(html):
    response = MagicMock()
    response.text = html
    return response


def test_catalog_extracts_product_metadata():
    html = create_product_html(
        "Test Book",
        "25.99",
        "Five",
        "catalogue/test-book_1/index.html"
    )

    session = MagicMock()
    session.get.return_value = create_mock_response(html)
    logger = MagicMock()

    with patch("scraper.core.catalog.TOTAL_PAGES", 1), \
         patch("scraper.core.catalog.DELAY", 0), \
         patch("scraper.core.catalog.time.sleep"):

        results = scrape_catalog(session, logger)

    assert len(results) == 1
    assert results[0]["name"] == "Test Book"
    assert results[0]["price_gbp"] == 25.99
    assert results[0]["rating"] == 5
    assert results[0]["url"].endswith(
        "catalogue/test-book_1/index.html"
    )

def test_catalog_extracts_multiple_products():
    html = (
        create_product_html(
            "Book One", "10.00", "Four",
            "catalogue/book-one/index.html"
        )
        +
        create_product_html(
            "Book Two", "15.50", "Three",
            "catalogue/book-two/index.html"
        )
    )

    session = MagicMock()
    session.get.return_value = create_mock_response(html)
    logger = MagicMock()

    with patch("scraper.core.catalog.TOTAL_PAGES", 1), \
         patch("scraper.core.catalog.DELAY", 0), \
         patch("scraper.core.catalog.time.sleep"):

        results = scrape_catalog(session, logger)

    assert len(results) == 2
    assert results[0]["name"] == "Book One"
    assert results[1]["name"] == "Book Two"

def test_catalog_retries_failed_request():
    html = create_product_html(
        "Retry Book",
        "12.99",
        "Five",
        "catalogue/retry-book/index.html"
    )

    session = MagicMock()
    session.get.side_effect = [
        Exception("Connection failed"),
        create_mock_response(html)
    ]

    logger = MagicMock()

    with patch("scraper.core.catalog.TOTAL_PAGES", 1), \
         patch("scraper.core.catalog.RETRIES", 2), \
         patch("scraper.core.catalog.DELAY", 0), \
         patch("scraper.core.catalog.time.sleep"):

        results = scrape_catalog(session, logger)

    assert len(results) == 1
    assert results[0]["name"] == "Retry Book"
    assert session.get.call_count == 2
    logger.warning.assert_called_once()

def test_catalog_logs_error_after_all_retries_fail():
    session = MagicMock()
    session.get.side_effect = Exception("Connection unavailable")
    logger = MagicMock()

    with patch("scraper.core.catalog.TOTAL_PAGES", 1), \
         patch("scraper.core.catalog.RETRIES", 2), \
         patch("scraper.core.catalog.DELAY", 0), \
         patch("scraper.core.catalog.time.sleep"):

        results = scrape_catalog(session, logger)

    assert results == []
    assert session.get.call_count == 2
    logger.error.assert_called_once()

def test_catalog_handles_page_with_no_products():
    session = MagicMock()
    session.get.return_value = create_mock_response(
        "<html><body><h1>No products found</h1></body></html>"
    )
    logger = MagicMock()

    with patch("scraper.core.catalog.TOTAL_PAGES", 1), \
         patch("scraper.core.catalog.DELAY", 0), \
         patch("scraper.core.catalog.time.sleep"):

        results = scrape_catalog(session, logger)

    assert results == []
    logger.error.assert_not_called()