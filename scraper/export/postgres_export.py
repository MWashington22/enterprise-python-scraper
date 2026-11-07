"""
PostgreSQL export module.

Responsible for:
- Connecting to PostgreSQL
- Creating the products table (if not exists)
- Inserting each product row
- Logging success or failure
"""

import psycopg2  # PostgreSQL client library
from scraper.config import DB_CONFIG  # Database credentials


def export_postgres(df, logger):
    """
    Exports the DataFrame to a PostgreSQL database.

    Parameters:
        df: pandas DataFrame containing product data
        logger: rotating logger instance
    """

    # ---------------------------------------------------------
    # STEP 1 — Connect to the database
    # ---------------------------------------------------------

    conn = psycopg2.connect(**DB_CONFIG)
    # ^ Connect using host, database, user, password

    cur = conn.cursor()
    # ^ Create a cursor for executing SQL commands


    # ---------------------------------------------------------
    # STEP 2 — Create table if it doesn't exist
    # ---------------------------------------------------------

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT,
            price_usd FLOAT,
            rating INT,
            availability TEXT,
            description TEXT,
            url TEXT
        )
    """)
    # ^ Ensures the table exists before inserting data


    # ---------------------------------------------------------
    # STEP 3 — Insert rows
    # ---------------------------------------------------------

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO products (name, price_usd, rating, availability, description, url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            row["Product Name"],
            float(row["Price (USD)"]),
            int(row["Rating"]),
            row["Availability"],
            row["Description"],
            row["Product URL"],
        ))
        # ^ Insert each row into the database


    # ---------------------------------------------------------
    # STEP 4 — Commit and close
    # ---------------------------------------------------------

    conn.commit()  # Save changes
    cur.close()    # Close cursor
    conn.close()   # Close connection

    logger.info("Data exported to PostgreSQL")
    # ^ Log successful export