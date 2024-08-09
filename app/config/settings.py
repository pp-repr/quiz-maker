from pydantic_settings import BaseSettings
from functools import lru_cache

import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI"
    DEBUG: bool = False

    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE")
    MYSQL_HOST: str = os.getenv("MYSQL_HOST")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT"))

    DATABASE_URL: str = f"mysql+pymysql://{MYSQL_USER}:%s@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}" % quote_plus(MYSQL_PASSWORD)

    SECRET_KEY: str = os.getenv("SECRET_KEY")

@lru_cache()
def get_settings() -> Settings:
    return Settings()
