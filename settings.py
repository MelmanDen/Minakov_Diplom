from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()



class Settings(BaseSettings):
    virus_total_api_key: str = Field(..., env="VIRUS_TOTAL_API_KEY")
    virus_total_scan_url: str = Field(..., env="VIRUS_TOTAL_SCAN_URL")
    virus_total_attempts: int = Field(..., env="VIRUS_TOTAL_ATTEMPTS")
    virus_total_interval: int = Field(..., env="VIRUS_TOTAL_INTERVAL")

    checkphish_scan_url: str = Field(..., env="CHECKPHISH_SCAN_URL")
    checkphish_status_url: str = Field(..., env="CHECKPHISH_STATUS_URL")
    checkphish_api_key: str = Field(..., env="CHECKPHISH_API_KEY")
    checkphish_attempts: int = Field(..., env="CHECKPHISH_ATTEMPTS")
    checkphish_interval: int = Field(..., env="CHECKPHISH_INTERVAL")
    time_in_cache: int = Field(..., env="TIME_IN_CACHE")

    api_version: str = Field(..., env="API_VERSION")

    redis_url: str = Field(..., env="REDIS_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

