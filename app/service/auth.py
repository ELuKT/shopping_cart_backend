from datetime import datetime, timedelta
from fastapi import status
from jwt import PyJWTError
from app.config.settings import get_sc_private_key, get_env_config, AppSettings
from app.config.settings import get_sc_jwk
from app.model.common import SCException, ErrorCode, Provider
from passlib.context import CryptContext
import jwt
from app.model.jwt.base_jwt import BaseJwt

from app.service.log_service import LogService
from .oauth import get_google_jwks

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encrypt_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)

def get_kid(jwt_token):
    return jwt.get_unverified_header(jwt_token).get('kid')

def generate_sc_jwt(email):
    expiration_seconds = get_env_config().JWT_EXP
    return jwt.encode(
        {
            'email': email,
            'exp': datetime.utcnow() + timedelta(seconds=float(expiration_seconds))
        },
        get_sc_private_key(),
        algorithm='RS256',
        headers={
            'kid': get_sc_jwk().get('kid')
        }
    )


def get_email_from_payload(payload) -> str:
    user_email = payload.get('email', None)
    if not user_email:
        LogService.error('payload does not contain email')
        raise SCException(status.HTTP_401_UNAUTHORIZED, ErrorCode.SC002)
    return user_email

# BaseJwt is protocol
async def extract_email_from_jwt(jwt_token: BaseJwt) -> str:
    return jwt_token.extract_email()
