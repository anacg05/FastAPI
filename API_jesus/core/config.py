import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost/jesus_api")
    # ↑ Coloque a senha do MySQL se tiver (ex: root:senha)
    APP_NAME: str = "Jesus API"
    APP_VERSION: str = "0.1.0"

settings = Settings()
