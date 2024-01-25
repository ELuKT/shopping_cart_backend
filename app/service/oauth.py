from functools import lru_cache
import uuid
import httpx
from oauthlib.oauth2 import WebApplicationClient
from pydantic import BaseModel
from app.config.settings import get_env_config, get_sc_jwk
import jwt
from functools import lru_cache
from app.model.common import SCException, ErrorCode, Provider
from app.model.entity import *
from .http_util import post_request
from fastapi import status

def generate_state():
    return str(uuid.uuid4())


class OpenIDConfig(BaseModel):
    issuer: str
    authorization_endpoint: str
    jwks_uri: str
    token_endpoint: str

# https://github.com/tiangolo/fastapi/issues/1985
@lru_cache()
def get_google_openid_config():
    env_config = get_env_config()
    config = httpx.get(env_config.GOOGLE_CONFIG_URL)
    return OpenIDConfig(**config.json())


@lru_cache()
def get_google_jwks():
    google_openid_config = get_google_openid_config()
    config = httpx.get(google_openid_config.jwks_uri)
    return config.json().get('keys')

_oauth_cli = WebApplicationClient(get_env_config().GOOGLE_OAUTH_CLIENT_ID)


def get_prepare_request_uri(openid_config: OpenIDConfig, state):
    env_config = get_env_config()
    return _oauth_cli.prepare_request_uri(
        openid_config.authorization_endpoint,
        redirect_uri=f'{env_config.BASE_URL}{env_config.BACKEND_OAUTH_REDIRECT_PATH}',
        scope=[env_config.GOOGLE_OAUTH_SCOPES],
        state=state,
    )


async def get_id_token(redirect_uri, state)->httpx.Response:
    google_openid_config = get_google_openid_config()
    env_config = get_env_config()
    req_url, headers, body = _oauth_cli.prepare_token_request(token_url=google_openid_config.token_endpoint,
                                                              authorization_response=redirect_uri,
                                                              redirect_url=f'{env_config.BASE_URL}{env_config.BACKEND_OAUTH_REDIRECT_PATH}',
                                                              state=state,
                                                              client_secret=env_config.GOOGLE_OAUTH_CLIENT_SECRET)

    return await post_request(req_url, headers, param=body)


_gmail_cli = WebApplicationClient(get_env_config().GMAIL_CLIENT_ID)


async def get_access_token_by_refresh_token() -> httpx.Response:
    google_openid_config = get_google_openid_config()
    env_config = get_env_config()
    req_url, headers, body = _gmail_cli.prepare_refresh_token_request(token_url=google_openid_config.token_endpoint,
                                                                      refresh_token=env_config.GMAIL_REFRESH_TOKEN,
                                                                      client_id=env_config.GMAIL_CLIENT_ID,
                                                                      client_secret=env_config.GMAIL_CLIENT_SECRET)
    return await post_request(req_url, headers, param=body)
