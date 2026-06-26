import os
import mysql.connector
import urllib.parse as urlparse

from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_connection():
    """
    Create and return a MySQL database connection.
    Supports individual credentials and URL-based configurations (Render/Heroku).
    """

    try:
        # Check if there is a unified database URL (common in production hosting)
        db_url = os.getenv("DATABASE_URL") or os.getenv("JAWSDB_URL") or os.getenv("CLEARDB_DATABASE_URL")

        if db_url:
            # Parse connection URL: mysql://user:password@host:port/database
            parsed = urlparse.urlparse(db_url)

            # Extract database name (remove leading slash)
            db_name = parsed.path[1:] if parsed.path else ""

            connection = mysql.connector.connect(
                host=parsed.hostname,
                port=parsed.port or 3306,
                user=parsed.username,
                password=parsed.password,
                database=db_name,
                connection_timeout=10,
                autocommit=False
            )
        else:
            # Fall back to separate environment variables
            connection = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=int(os.getenv("DB_PORT", 3306)),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", ""),
                database=os.getenv("DB_NAME", "smart_expense_tracker"),
                connection_timeout=10,
                autocommit=False
            )

        if connection.is_connected():
            return connection

        raise Exception("Unable to connect to database.")

    except Error as e:

        print("=" * 60)
        print("DATABASE CONNECTION ERROR")
        print(e)
        print("=" * 60)

        raise