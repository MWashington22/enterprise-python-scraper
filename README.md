Enterprise‑Grade E‑Commerce Scraper
A modular, scalable, production‑style scraping pipeline engineered for reliability, clarity, and long‑term automation.

Overview
This project is a fully modular, enterprise‑grade web scraping system built to demonstrate professional engineering standards for automation, data extraction, and workflow orchestration.
It uses BooksToScrape.com as a safe demo source, but the architecture is designed for real‑world e‑commerce, SaaS dashboards, real estate platforms, and large‑scale data pipelines.
The scraper features:
- Clean, maintainable architecture
- Resilient networking with retry logic
- Concurrent scraping for performance
- Automated daily scheduling
- Multi‑format export (CSV, Excel, JSON, PostgreSQL)
- A pipeline‑driven design suitable for production environments

Key Features
- Modular Architecture — clean separation of concerns across core, utils, and export layers
- Retry‑Enabled Networking — shared session with automatic backoff
- Concurrent Scraping — ThreadPoolExecutor for high‑performance product extraction
- Live GBP → USD Conversion — with fallback for API failures
- Data Cleaning & Normalization — deduplication and structured output
- Multi‑Format Export — CSV, Excel, JSON, PostgreSQL
- Daily Automation — scheduled runs at 2:00 AM
- Rotating Logs — full observability and long‑term traceability

Architecture
[ Session ]
     ↓
[ Catalog Scraper ] → product metadata
     ↓
[ Product Scraper ] → enriched product data
     ↓
[ Pipeline ] → cleaning, dedupe, normalization
     ↓
[ Export Layer ] → CSV, Excel, JSON, PostgreSQL



Folder Structure
scraper/
│── __init__.py
│── main.py
│── config.py
│── core/
│   ├── __init__.py
│   ├── session.py
│   ├── catalog.py
│   ├── product.py
│   ├── currency.py
│   ├── pipeline.py
│── utils/
│   ├── __init__.py
│   ├── logger.py
│   ├── parsing.py
│── export/
│   ├── __init__.py
│   ├── csv_export.py
│   ├── excel_export.py
│   ├── json_export.py
│   ├── postgres_export.py
│── data/
│── logs/



Tech Stack
- Python 3.10+
- Requests
- BeautifulSoup + lxml
- ThreadPoolExecutor
- Pandas
- Psycopg2
- Schedule
- Tqdm

How to Run
1. Install dependencies
pip install -r requirements.txt


2. Run the scraper immediately
python -m scraper.main


3. Automated daily runs
The scraper automatically runs every day at 2:00 AM.

Exports
After each run, the following files are generated in scraper/data/:
- products.csv
- products.xlsx
- products.json
If PostgreSQL is configured, data is also inserted into the products table.

Why This Scraper Is Enterprise‑Grade
- Modular, layered architecture — easy to extend and maintain
- Resilient networking — retry logic, backoff, and session reuse
- Observability — rotating logs with timestamps and structured messages
- Scalable design — concurrency and clean separation of responsibilities
- Production‑style pipeline — ingestion → enrichment → cleaning → export




