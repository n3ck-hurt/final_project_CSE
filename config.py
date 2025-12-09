import os


class Config:
    """Configuration sourced from environment variables."""

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "cse_final_project")
    DB_PORT = int(os.getenv("DB_PORT", 3306))

    JSON_SORT_KEYS = False


