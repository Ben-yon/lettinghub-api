from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    API_V1_STR: str = "/api/v1"
    APP_NAME: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY: str
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 3600
    ALGORITHM: str = "HS256"
    POSTGRES_URL: str

    class Config:
        env_file = ".env"


settings = Settings()