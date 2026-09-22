from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "video-hosting-api"
    environment: str = "development"

    secret_key: str
    access_token_expire_minutes: int = 60
    algorithm: str = "HS256"

    database_url: str
    redis_url: str = "redis://localhost:6379/0"

    s3_endpoint_url: str
    s3_access_key: str
    s3_secret_key: str
    s3_bucket_name: str = "videos"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
