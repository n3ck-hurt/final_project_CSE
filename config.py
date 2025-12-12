# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration for the Flask app."""
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'estares223')
    MYSQL_DB = os.getenv('MYSQL_DB', 'sari-sari_store')
    MYSQL_CURSORCLASS = 'DictCursor'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    JSON_SORT_KEYS = False