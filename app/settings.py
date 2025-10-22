from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class CommonConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env" if os.path.exists(".env") else ".env.example",
        extra="ignore",
        env_ignore_empty=True)
    
class Settings(CommonConfig):
    YOUTUBE_API_KEY: str
    REDDIT_CLIENT: str
    REDDIT_TOKEN: str


settings = Settings()