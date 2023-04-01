from pydantic import BaseSettings


class Settings(BaseSettings):
    EMAIL_IGNORE: bool = False

    EMAIL_HOST: str = 'smtp.163.com'
    EMAIL_SMTP_PORT: int = 25
    EMAIL_USER: str = ''
    EMAIL_PWD: str = ''

    PRIVATE_KEY: str = ''
    PUBLIC_KEY: str = ''

    class Config:
        env_prefix = 'AUTH_'
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
