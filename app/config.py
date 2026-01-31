import os

from dotenv import load_dotenv

# dev
load_dotenv()


class Settings:
    ENV: str = os.getenv("ENV", "development")
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "127.0.0.1")
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"


settings = Settings()
