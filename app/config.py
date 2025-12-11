from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    MASTER_DB: str = "master_db"
    JWT_SECRET: str = "supersecretkey"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 3600

    class Config:
        env_file = ".env"

settings = Settings()
