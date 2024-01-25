import json
from typing import Optional
from pydantic import BaseSettings
from functools import lru_cache
import base64

class AppSettings(BaseSettings):
    # can use uppercase in env file, uppercase env has priority
    MONGODB_URL: str
    MONGODB_DATABASE_NAME: str
    GOOGLE_OAUTH_CLIENT_ID: str
    GOOGLE_OAUTH_CLIENT_SECRET: str
    GOOGLE_CONFIG_URL: str
    GOOGLE_OAUTH_SCOPES: str
    GOOGLE_SENDING_EMAIL_API: str
    BACKEND_OAUTH_REDIRECT_PATH: str
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASSWORD: str
    JWT_EXP: str
    GMAIL_CLIENT_ID: str
    GMAIL_CLIENT_SECRET: str
    GMAIL_REFRESH_TOKEN: str
    GMAIL_SCOPES: str
    GMAIL_USER: str
    BACKEND_EMAIL_VALIDATE_REGISTRATION_PATH: str
    SC_PRIVATE_KEY: str
    SC_JWK: str
    # env file 'DOCS_URL=' gives empty string, remove 'DOCS_URL=' from env file use default None
    DOCS_URL: Optional[str] = None
    BASE_URL: str

    class Config():
        env_file = '.env'


@lru_cache()
def get_env_config():
    return AppSettings()


@lru_cache()
def get_sc_private_key():
    return base64.b64decode(get_env_config().SC_PRIVATE_KEY).decode()

@lru_cache()
def get_sc_jwk():
    return json.loads(get_env_config().SC_JWK)
 