from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from httpx import Response
from app.config.jwt_bearer import get_current_user
from app.model.common import SCException, ErrorCode, AuthMethod
from app.model.entity import User
from app.model.jwt.google_id_token import GoogleIdToken
from app.model.jwt.shopping_cart_jwt import ShoppingCartJwt
from app.model.req.user_req import UserReq
import asyncio
from app.config.redis_cache import RedisCache
from app.service.auth import (
    encrypt_password,
    generate_sc_jwt,
    verify_password,
    extract_email_from_jwt,
)
from app.service.email import send_validate_email
from app.service.user import get_user, insert_user, update_user
from app.service.oauth import (
    OpenIDConfig,
    generate_state,
    get_google_openid_config,
    get_prepare_request_uri,
    get_id_token,
)
from app.service.log_service import LogService

router = APIRouter()


@router.post('/register')
async def register(user_req: UserReq, state: str = Depends(generate_state)):
    LogService.info('A new user begin register')
    user = await get_user(User.email == user_req.email)

    if user:
        raise SCException(status.HTTP_409_CONFLICT, ErrorCode.SC008)

    await insert_user(email=user_req.email, hashed_password=encrypt_password(user_req.password), is_validated=False, state=state, auth_method=AuthMethod.SC.value, records=[])
    loop = asyncio.get_event_loop()
    loop.create_task(send_validate_email(user_req.email, state))


@router.get('/validate-registration', response_model=None)
async def validate_registration(state: str, email: str):
    user: User = await get_user(User.email == email, User.state == state)
    if not user:
        raise SCException(status.HTTP_404_NOT_FOUND, ErrorCode.SC004)
    await update_user(user, {User.is_validated: True})


@router.post('/get-sc-token')
async def get_sc_token(user_req: UserReq):
    LogService.info('Get access token begin')
    user: User = await get_user(User.email == user_req.email)
    if not user:
        raise SCException(status.HTTP_404_NOT_FOUND, ErrorCode.SC003)
    if user.auth_method != AuthMethod.SC.value:
        raise SCException(status.HTTP_403_FORBIDDEN, ErrorCode.SC007)
    if not verify_password(user_req.password, user.hashed_password):
        raise SCException(status.HTTP_404_NOT_FOUND, ErrorCode.SC003)

    shopping_cart_jwt = generate_sc_jwt(user_req.email)
    LogService.info('Get access token ends')
    return {'shopping_cart_jwt': shopping_cart_jwt}


@router.post('/resend-email')
async def resend_email(user: User = Depends(get_current_user), state: str = Depends(generate_state)):
    LogService.info('Resend email begin')
    if user.auth_method == AuthMethod.SC.value:
        await update_user(user, {User.state: state})
        loop = asyncio.get_event_loop()
        loop.create_task(send_validate_email(user.email, state))
    else:
        raise SCException(status.HTTP_403_FORBIDDEN, ErrorCode.SC007)


@router.get('/oauth-login')
async def oauth_login(
        auth_state: str = Depends(generate_state),
        google_openid_config: OpenIDConfig = Depends(
            get_google_openid_config)
):
    LogService.info('Begin google oauth login')
    authorization_request_url = get_prepare_request_uri(
        google_openid_config, auth_state)
    await RedisCache.hset(auth_state, ['AuthMethod', AuthMethod.GOOGLE.value])
    await RedisCache.expire(auth_state)
    LogService.info('Redirect to login page')
    return RedirectResponse(authorization_request_url)


@router.get('/get_token')
async def get_token(
        state: str,
        request: Request
):
    LogService.info('Begin to get id token')
    info: dict = await RedisCache.hgetall(state)
    if not info:
        LogService.error('Can not find state in cache')
        raise SCException(status.HTTP_400_BAD_REQUEST, ErrorCode.SC009)

    res: Response = await get_id_token(str(request.url).replace(
                                               'http', 'https'),
                                           state)
    if res.is_error:
        LogService.error('Fail to get id token', res.json())
        raise SCException(status.HTTP_503_SERVICE_UNAVAILABLE, ErrorCode.SC005)

    shopping_cart_jwt: str = res.json().get('id_token')
    jwt_token = GoogleIdToken(shopping_cart_jwt)
    email = await extract_email_from_jwt(jwt_token)
    user = await get_user(User.email == email)

    if user is None:
        LogService.error('User not find, insert new user', res.json())
        await insert_user(email=email, hashed_password='', is_validated=True, state='', auth_method=AuthMethod.GOOGLE.value, records=[])
    elif user.auth_method != AuthMethod.GOOGLE.value:
        LogService.error('User already in db, but auth_method is not google')
        raise SCException(status.HTTP_409_CONFLICT, ErrorCode.SC006)

    await RedisCache.delete(state)

    return {'shopping_cart_jwt': shopping_cart_jwt}
