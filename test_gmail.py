import os
import smtplib
from email.message import EmailMessage

gmail = os.getenv("GMAIL_ADDRESS")
password = os.getenv("GMAIL_APP_PASSWORD")

if not gmail or not password:
    raise ValueError("Gmail credentials are missing.")

message = EmailMessage()
message["Subject"] = "Enterprise Scraper - Email Test"
message["From"] = gmail
message["To"] = gmail

message.set_content(
    "Success! Your Python Enterprise Scraper "
    "can now send automated Gmail notifications."
)

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail, password)
        server.send_message(message)

    print("SUCCESS: Test email sent!")

except Exception as e:
    print(f"EMAIL ERROR: {e}")