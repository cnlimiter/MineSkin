from pydantic import BaseSettings


class Settings(BaseSettings):
    HOST: str = '127.0.0.1'
    PORT: int = 3306
    DB: int = 1

    class Config:
        env_prefix = 'REDIS_'
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
