from pydantic import BaseSettings
from config.app import settings as app_settings

"""
配置参考loguru
"""


class Settings(BaseSettings):
    LEVEL: str = "INFO"
    PATH: str = app_settings.BASE_PATH + "/storage/logs/MineSkin-{time:YYYY-MM-DD}.log"
    RETENTION: str = "14 days"

    class Config:
        env_prefix = 'LOG_'
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
