from pydantic import BaseSettings


class Settings(BaseSettings):
    TTL: int = 60 * 24 * 8
    SECRET_KEY: str = ""
    ALGORITHM: str = 'HS256'

    class Config:
        env_prefix = 'JWT_'
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
