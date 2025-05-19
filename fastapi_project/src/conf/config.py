from typing import Any
from pydantic import ConfigDict, field_validator, EmailStr
from pydantic_settings import BaseSettings
from pathlib import Path
import os



BASE_DIR = Path(__file__).resolve().parent.parent  # src/

if os.getenv("SPHINX_BUILD"):
    ENV_PATH = BASE_DIR / ".env.example"   # специальный файл для доков
else:
    ENV_PATH = BASE_DIR / ".env"

# ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    These settings configure database, JWT, email, Redis, and Cloudinary services.
    Environment variables are read from a `.env` file.
    """
    DB_URL: str
    SECRET_KEY_JWT: str
    ALGORITHM: str
    MAIL_USERNAME: EmailStr
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME:str
    REDIS_DOMAIN: str
    REDIS_PORT: int
    REDIS_PASSWORD: str | None = None
    CLOUDINARY_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    @field_validator("ALGORITHM")
    @classmethod
    def validate_algorithm(cls, v: Any):
        """
        Validate the JWT algorithm to be one of the accepted options.

        :param v: Algorithm name.
        :type v: str
        :raises ValueError: If algorithm is not "HS256" or "HS512".
        :return: Validated algorithm.
        :rtype: str
        """
        if v not in ["HS256", "HS512"]:
            raise ValueError("algorithm must be HS256 or HS512")
        return v


    model_config = ConfigDict(extra='ignore', env_file=ENV_PATH, env_file_encoding="utf-8")  # noqa


config = Settings()



