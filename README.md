# Enterprise Python Web Scraper & Price Intelligence Platform

An automated Python-based web scraping and price intelligence platform designed to collect product data, monitor pricing, generate reports, and deliver automated email notifications through an interactive analytics dashboard.

Built with Python, BeautifulSoup, Pandas, Streamlit, and Plotly.

---

## Project Overview

This project demonstrates an end-to-end data extraction and automation solution.

The application collects product information from an e-commerce catalog, processes and validates the extracted data, converts prices from GBP to USD, tracks historical pricing, identifies price changes, and generates reports.

An interactive Streamlit dashboard provides a centralized interface for reviewing product information and analyzing pricing trends.

The current implementation successfully collects 1,000 products across 100 catalog pages from Books to Scrape.

## Key Features

### Web Scraping & Data Extraction
- Automated extraction of product information.
- Multi-page catalog scraping.
- Product name, price, rating, availability, description, and URL collection.
- Concurrent processing using ThreadPoolExecutor.
- Retry handling and session management.

### Data Processing & Validation
- GBP to USD currency conversion.
- Data cleaning and validation.
- Duplicate product URL detection.
- Missing and invalid field detection.
- Automated validation reporting.

### Price Intelligence
- Historical product price tracking.
- Price drop and price increase detection.
- Percentage change calculations.
- Top price drop reporting.
- CSV-based price history storage.

### Automated Reporting & Notifications
- CSV, Excel, and JSON exports.
- Optional PostgreSQL data export.
- Automated email notifications through Gmail SMTP.
- Daily scheduled execution through Windows Task Scheduler.
- Application logging.

### Interactive Analytics Dashboard
- Streamlit-powered web interface.
- Product catalog browsing and searching.
- Price filtering.
- Product pricing metrics.
- Historical price analysis.
- Price drop and increase reports.
- Interactive Plotly visualizations.

## Dashboard

The application includes four main dashboard sections:

| Section | Description |
|---|---|
| Overview | Product totals, average prices, and pricing metrics |
| Price Analytics | Historical pricing and product price analysis |
| Product Catalog | Searchable and filterable product database |
| Price Alerts | Price drops and price increases |

Dashboard screenshots will be added here.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Requests | HTTP requests |
| BeautifulSoup | HTML parsing and extraction |
| Pandas | Data processing and analysis |
| ThreadPoolExecutor | Concurrent scraping |
| Streamlit | Interactive dashboard |
| Plotly | Data visualization |
| PostgreSQL | Optional database integration |
| SMTP | Automated email notifications |
| Git & GitHub | Version control and project hosting |

## Project Structure

```text
enterprise-python-scraper/
│
├── .gitignore
├── README.md
├── dashboard.py
├── requirements.txt
├── test_gmail.py
│
└── scraper/
    ├── __init__.py
    ├── config.py
    ├── main.py
    │
    ├── core/
    │   ├── __init__.py
    │   ├── catalog.py
    │   ├── currency.py
    │   ├── email_alerts.py
    │   ├── pipeline.py
    │   ├── price_report.py
    │   ├── price_tracker.py
    │   ├── product.py
    │   ├── session.py
    │   └── validation.py
    │
    ├── export/
    │   ├── __init__.py
    │   ├── csv_export.py
    │   ├── excel_export.py
    │   ├── json_export.py
    │   └── postgres_export.py
    │
    └── utils/
        ├── __init__.py
        ├── logger.py
        └── parsing.py
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/MWashington22/enterprise-python-scraper.git
```

### 2. Navigate to the project directory

```bash
cd enterprise-python-scraper
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Running the Application

### Run the scraper

```bash
python -m scraper.main
```

The scraper executes the data collection and processing pipeline, including validation, price tracking, reporting, and configured notifications.

### Launch the dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open in your browser.

## Email Configuration

Email notifications use Gmail SMTP.

Configure the following Windows environment variables:

- `GMAIL_ADDRESS`
- `GMAIL_APP_PASSWORD`

PowerShell example:

```powershell
$env:GMAIL_ADDRESS="your-email@gmail.com"
$env:GMAIL_APP_PASSWORD="your-app-password"
```

Use a Gmail App Password rather than your regular Google account password.

Never commit actual credentials, passwords, or API keys to GitHub.

## Generated Data

The application generates data files under:

```text
scraper/data/
```

These include:

- `products.csv`
- `products.xlsx`
- `products.json`
- `price_history.csv`
- `price_drops.csv`
- `price_increases.csv`
- `top_price_drops.csv`

Generated files and application logs are excluded from the public Git repository.

## Future Development

Potential enhancements include:

- Additional e-commerce website integrations.
- Historical pricing visualization improvements.
- Advanced product comparison.
- Database-driven analytics.
- Configurable scraping schedules.
- Expanded automated notification options.
- Additional dashboard reporting capabilities.

## Project Purpose

This project demonstrates practical experience in:

- Python application development.
- Web scraping and data extraction.
- Workflow automation.
- Data processing and validation.
- Price monitoring and reporting.
- Database integration.
- Interactive dashboard development.
- Software project organization and version control.

## Author

**MWashington22**

GitHub: https://github.com/MWashington22

---

*This project uses Books to Scrape as a demonstration data source. When adapting the scraper to other websites, comply with their terms of service, robots.txt policies, and applicable rate limits.*