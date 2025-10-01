import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")  # Pega a variável do sistema
    APP_NAME: str = "Jesus API"
    APP_VERSION: str = "0.1.0"

settings = Settings()

print(f"DATABASE_URL: {settings.DATABASE_URL}")