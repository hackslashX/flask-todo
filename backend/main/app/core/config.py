""" Fetch configuration from environment variables. """

from datetime import timedelta

from pydantic import BaseSettings


class DBSettings(BaseSettings):
    """Database settings"""

    DATABASE_CONNECTION_URL: str = ""
    DATABASE_HOST: str = ""
    DATABASE_PORT: str = ""
    DATABASE_USERNAME: str = ""
    DATABASE_PASSWORD: str = ""
    DATABASE_NAME: str = ""


class JWTSettings(BaseSettings):
    """JWT settings"""

    JWT_SECRET_KEY: str = ""
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(days=30)


class Settings(BaseSettings):
    """Main settings"""

    API_V1_STR: str = "/api/v1"
    db = DBSettings()
    db.DATABASE_CONNECTION_URL = db.DATABASE_CONNECTION_URL.format(**db.dict())

    jwt = JWTSettings()


settings = Settings()
