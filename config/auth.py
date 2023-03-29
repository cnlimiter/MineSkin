from pydantic import BaseSettings


class Settings(BaseSettings):
    EMAIL_IGNORE: bool = False

    class Config:
        env_prefix = 'AUTH_'
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
