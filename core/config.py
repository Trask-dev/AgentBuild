from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    DB_URL: str = os.getenv("DB_URL")
    HOST: str = os.getenv("SERVER_HOST")
    PORT: int = int(os.getenv("SERVER_PORT"))

settings = Settings()