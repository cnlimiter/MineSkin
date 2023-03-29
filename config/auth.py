from pydantic import BaseSettings


class Settings(BaseSettings):
    EMAIL_IGNORE: bool = False

    PRIVATE_KEY: str = ''
    PUBLIC_KEY: str = ''

    class Config:
        env_prefix = 'AUTH_'
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
