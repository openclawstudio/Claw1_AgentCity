from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    WORLD_WIDTH: int = 100
    WORLD_HEIGHT: int = 100
    TICK_RATE: float = 1.0
    OPENAI_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()