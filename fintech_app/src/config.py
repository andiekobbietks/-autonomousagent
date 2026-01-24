from pydantic_settings import BaseSettings

from pydantic import ConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./fintech.db"
    secret_key: str = "your-secret-key"

    model_config = ConfigDict(env_file=".env")

settings = Settings()
