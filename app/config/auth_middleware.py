import logging
from fastapi import Request, status
from app.model.common.enums import ErrorCode
from app.model.common.sc_exception import SCException
from app.model.entity.user import User
from app.service import get_user, extract_email_from_jwt
from .sc_exception_handlers import sc_exception_handler
from starlette.middleware.base import BaseHTTPMiddleware


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path not in ['/docs', '/openapi.json', '/v1/auth/oauth_redirect', '/v1/auth/get_token', '/v1/auth/register', '/v1/auth/get-sc-token', '/v1/auth/validate-registration', '/v1/refresh/']:
            jwt_token = None
            if "Authorization" in request.headers:
                jwt_token = request.headers["Authorization"].replace(
                    "Bearer ", "")

            if not jwt_token:#
                return await sc_exception_handler(request, SCException(status.HTTP_401_UNAUTHORIZED, ErrorCode.SC001))

            try:
                email = extract_email_from_jwt(jwt_token)

                user = await get_user(User.email == email)

                if not user:
                    logging.exception('cant find user in db')
                    raise SCException(status.HTTP_401_UNAUTHORIZED, ErrorCode.SC004)
                request.user = user
            except SCException as e:
                return await sc_exception_handler(request, e)
        response = await call_next(request)
        return response
