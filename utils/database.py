import os
import mysql.connector
import mysql.connector.pooling
import urllib.parse as urlparse

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global database pool instance
db_pool = None

def get_connection():
    """
    Get a connection from the global MySQL connection pool.
    Initializes the pool on first request. Supports Database URL and localhost configurations.
    """
    global db_pool
    if db_pool is None:
        try:
            # Check if there is a unified database URL (production cloud hosting)
            db_url = os.getenv("DATABASE_URL") or os.getenv("JAWSDB_URL") or os.getenv("CLEARDB_DATABASE_URL")

            if db_url:
                # Clean any surrounding quotes (which sometimes happen when users enter quotes on Render)
                db_url = db_url.strip('"\'')
                # Parse connection URL: mysql://user:password@host:port/database
                parsed = urlparse.urlparse(db_url)
                db_name = parsed.path[1:] if parsed.path else ""

                db_pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name="smart_expense_pool",
                    pool_size=10,
                    host=parsed.hostname,
                    port=parsed.port or 3306,
                    user=parsed.username,
                    password=parsed.password,
                    database=db_name,
                    connection_timeout=15
                )
            else:
                # Fall back to separate environment variables (local development)
                db_pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name="smart_expense_pool",
                    pool_size=10,
                    host=os.getenv("DB_HOST", "localhost"),
                    port=int(os.getenv("DB_PORT", 3306)),
                    user=os.getenv("DB_USER", "root"),
                    password=os.getenv("DB_PASSWORD", ""),
                    database=os.getenv("DB_NAME", "smart_expense_tracker"),
                    connection_timeout=15
                )

        except Exception as e:
            print("=" * 60)
            print("DATABASE POOL INITIALIZATION ERROR")
            print(e)
            print("=" * 60)
            # Ensure pool is reset so it retries next time
            db_pool = None
            raise

    try:
        connection = db_pool.get_connection()
        if connection.is_connected():
            return connection
        raise Exception("Retrieved connection is not connected.")
    except Exception as e:
        print("=" * 60)
        print("DATABASE GET CONNECTION FROM POOL ERROR")
        print(e)
        print("=" * 60)
        # Reset pool to trigger re-initialization on failure
        db_pool = None
        raise
