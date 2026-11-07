import os
import smtplib
from pathlib import Path
from email.message import EmailMessage

import pandas as pd


def send_price_alerts(logger):
    logger.info("Checking for price-drop email alerts...")

    # Retrieve Gmail credentials
    gmail_address = os.getenv("GMAIL_ADDRESS")
    app_password = os.getenv("GMAIL_APP_PASSWORD")

    if not gmail_address or not app_password:
        logger.error("Gmail credentials are not configured.")
        return

    # Locate price-drop report
    data_dir = Path(__file__).resolve().parents[1] / "data"
    drops_file = data_dir / "price_drops.csv"

    if not drops_file.exists():
        logger.warning("Price-drop report not found.")
        return

    drops = pd.read_csv(drops_file)

    if drops.empty:
        logger.info("No price drops detected. No email sent.")
        return

    # Build email
    message = EmailMessage()

    message["Subject"] = (
        f"Price Alert: {len(drops)} Products Decreased in Price"
    )

    message["From"] = gmail_address
    message["To"] = gmail_address

    body = [
        "Your scraper detected the following price decreases:",
        ""
    ]

    for _, product in drops.head(20).iterrows():
        body.extend([
            f"Product: {product['Product Name']}",
            f"Previous Price: ${product['previous_price']:.2f}",
            f"Current Price: ${product['current_price']:.2f}",
            f"Price Difference: ${product['price_difference']:.2f}",
            f"Percentage Change: {product['percentage_change']:.2f}%",
            f"Product URL: {product['Product URL']}",
            "-" * 50
        ])

    if len(drops) > 20:
        body.append(
            f"Additional products: {len(drops) - 20}"
        )

    message.set_content("\n".join(body))

    # Send email securely
    try:
        with smtplib.SMTP_SSL(
            "smtp.gmail.com", 465
        ) as server:

            server.login(gmail_address, app_password)

            server.send_message(message)

        logger.info("Price alert email sent successfully.")

    except Exception:
        logger.exception("Failed to send price alert email.")