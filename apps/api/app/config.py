from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "postgresql+psycopg://smma:smma@127.0.0.1:5433/smma"
    redis_url: str = "redis://localhost:6379/0"
    allowed_origin: str = "http://localhost:3000"
    session_cookie_secure: bool = False
    session_ttl_hours: int = 168

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
