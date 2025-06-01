from pydantic import BaseSettings

class Settings(BaseSettings):
    DELIVERY_DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()