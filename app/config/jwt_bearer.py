from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, status, Depends
from app.model.common.enums import ErrorCode
from app.model.common.sc_exception import SCException
from app.model.entity.user import User
from app.model.jwt.base_jwt import BaseJwt
from app.service.oauth import get_google_jwks
from app.service.user import get_user
from app.service.auth import extract_email_from_jwt, get_kid
from app.service.log_service import LogService
from app.model.jwt.base_jwt import BaseJwt
from app.model.jwt.google_id_token import GoogleIdToken
from app.model.jwt.shopping_cart_jwt import ShoppingCartJwt
from app.config.settings import get_sc_jwk

jwt_bearer = HTTPBearer()

async def get_current_user(credential: HTTPAuthorizationCredentials = Depends(jwt_bearer)):
    if not credential:
        raise SCException(status.HTTP_401_UNAUTHORIZED, ErrorCode.SC001)
    
    jwt_token = None
    token_kid = get_kid(credential.credentials)
    if get_sc_jwk().get('kid') == token_kid:
        jwt_token = ShoppingCartJwt(credential.credentials)
    elif next((jwk for jwk in get_google_jwks() if jwk.get('kid') == token_kid), None):
        jwt_token = GoogleIdToken(credential.credentials)
    if not jwt_token:
        raise SCException(status.HTTP_401_UNAUTHORIZED, ErrorCode.SC001)
    email = await extract_email_from_jwt(jwt_token)

    user = await get_user(User.email == email)

    if not user:
        LogService.error('cant find user in db')
        raise SCException(status.HTTP_404_NOT_FOUND, ErrorCode.SC004)
    return user
    