import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# 始终从 backend/ 目录加载 .env（config.py → src/core/ → 上溯三级到 backend/）
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env'))

class Settings(BaseSettings):
    DB_URL: str = os.getenv("DB_URL")
    HOST: str = os.getenv("SERVER_HOST")
    PORT: int = int(os.getenv("SERVER_PORT"))

settings = Settings()