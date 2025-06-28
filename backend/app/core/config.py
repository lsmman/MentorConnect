from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET: str = "dev-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    DB_URL: str = "sqlite:///./app.db"
    PROFILE_IMG_DIR: str = "./profile_images"

settings = Settings()
