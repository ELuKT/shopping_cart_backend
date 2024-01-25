from app.config.settings import get_sc_jwk
from app.model.common import SCException, ErrorCode
from jwt import PyJWTError, decode, PyJWK, get_unverified_header
from fastapi import status
from app.service.auth import get_email_from_payload, get_kid
from app.service.oauth import get_google_jwks, get_google_openid_config, OpenIDConfig
from app.config.settings import  get_env_config, AppSettings

class GoogleIdToken:
    def __init__(self, jwt_token) -> None:
        self.jwt_token = jwt_token

    def extract_email(self)->str:
        token_kid = get_kid(self.jwt_token)
        jwk = next((jwk for jwk in get_google_jwks() if jwk.get('kid') == token_kid), None)
        public_key = PyJWK(jwk).key

        google_openid_config: OpenIDConfig = get_google_openid_config()
        env_config: AppSettings = get_env_config()
        try:
            payload = decode(self.jwt_token,
                                public_key,
                                algorithms=['RS256'],
                                audience=env_config.GOOGLE_OAUTH_CLIENT_ID,
                                issuer=google_openid_config.issuer,
                                leeway=5)
        except PyJWTError:
            raise SCException(status.HTTP_401_UNAUTHORIZED, ErrorCode.SC001)
        return get_email_from_payload(payload)