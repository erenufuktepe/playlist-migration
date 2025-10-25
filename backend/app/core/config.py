from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    CORS_ORIGINS: list[str] = ["*"]

    TOKEN_REFRESH_SKEW: int = 60

    SPOTIFY_ENDPOINT: str
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    SPOTIFY_REDIRECT_URI: str

    APPLE_TEAM_ID: str
    APPLE_KEY_ID: str
    APPLE_PRIVATE_KEY_PATH: str
    APPLE_TOKEN_TTL_SECONDS: int = 3600

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

settings = Settings()
