from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATA_BACKEND: str = "local"  # "s3" | "local"
    AWS_REGION: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    S3_BUCKET: Optional[str] = None
    S3_OBJECT_KEY: str = "today.json"

    TEAMLIST_CSV_URL: str

    KENPOM_EMAIL: Optional[str] = None
    KENPOM_PASSWORD: Optional[str] = None
    KENPOM_COOKIE: Optional[str] = None

    ADMIN_TOKEN: str = "change-me"

    USER_AGENT: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    HOST_DELAY_MS: int = 2000  # 2s
    
    class Config:
        env_file = ".env"

settings = Settings()
