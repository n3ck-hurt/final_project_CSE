import mysql.connector

from config import Config


def get_db_connection():
    """Return a new MySQL connection using env-driven settings."""
    return mysql.connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        port=Config.DB_PORT,
    )


