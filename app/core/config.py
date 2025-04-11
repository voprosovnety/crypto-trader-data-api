import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Crypto Trader Data API"
    API_VERSION: str = "v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DATABASE_URL_SYNC: str = os.getenv("DATABASE_URL_SYNC")

    if not DATABASE_URL or not DATABASE_URL_SYNC:
        raise ValueError("One of DATABASE_URL not found in .env")


settings = Settings()
