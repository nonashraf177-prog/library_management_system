# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Library Management System"
    DATABASE_URL: str = "sqlite:///./library.db"  # مبدئياً sqlite للسهولة
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY_123" # غيريه بعدين
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()