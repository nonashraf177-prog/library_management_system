# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Library Management System"
    DATABASE_URL: str = "sqlite:///./library.db" 
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY_123" #
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()