from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_NAME: str
    VERSION: str
    SERVER_NAME: str
    URL: str
    DOMAINS: List[str]

    class Config:
        env_prefix = 'INFO_'
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
