from app.config.settings import get_sc_jwk
from app.model.common import SCException, ErrorCode
from jwt import PyJWTError, decode, PyJWK
from fastapi import status
from app.service.auth import get_email_from_payload


class ShoppingCartJwt:
    def __init__(self, jwt_token) -> None:
        self.jwt_token = jwt_token

    def extract_email(self)->str:
        public_key = PyJWK(get_sc_jwk()).key
        try:
            payload = decode(self.jwt_token,
                                public_key,
                                algorithms=['RS256'])
        except PyJWTError:
            raise SCException(status.HTTP_401_UNAUTHORIZED, ErrorCode.SC001)
        return get_email_from_payload(payload)