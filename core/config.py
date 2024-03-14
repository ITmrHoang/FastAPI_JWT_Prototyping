from pydantic import BaseSettings
from decouple import config
from pathlib import Path

BASE_DIR =  Path(__file__).parent.parent

class Settings(BaseSettings):
    DATABASE_PORT: int = 6500
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str

    class Config:
        env_file = './.env'


settings = Settings()