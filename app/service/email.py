from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config.redis_cache import RedisCache
from app.config.settings import get_env_config
import base64
from app.model.common import SCException, ErrorCode, Hardcode, RedisKeys
from app.service.log_service import LogService
from .http_util import post_request
from .oauth import get_access_token_by_refresh_token
from fastapi import status


async def _get_access_token():

    access_token = await RedisCache.get_cache(RedisKeys.EMAIL_TOKEN)

    if not access_token:
        res = await get_access_token_by_refresh_token()

        if res.is_error:
            # invalid refresh token may cause {'error': 'invalid_grant', 'error_description': 'Bad Request'}
            LogService.error(res.json())
            raise SCException(status.HTTP_503_SERVICE_UNAVAILABLE, ErrorCode.SC005)

        access_token = res.json().get('access_token')

        if not access_token:
            raise SCException(status.HTTP_503_SERVICE_UNAVAILABLE, ErrorCode.SC005)

        # expire cache before the token expired
        await RedisCache.set_cache(RedisKeys.EMAIL_TOKEN, access_token, ex=3000)

    return access_token


async def send_validate_email(to_user: str, state):
    LogService.info('Sending email begin')
    try:
        access_token = await _get_access_token()
        env_config = get_env_config()

        message = MIMEMultipart()
        formatter={
            'user': to_user[0:to_user.find('@')],
            'validate_registration_url': f'{env_config.BASE_URL}{env_config.BACKEND_EMAIL_VALIDATE_REGISTRATION_PATH}?state={state}&email={to_user}'
        }
        content = MIMEText(Hardcode.EMAIL_Content.value.format(**formatter), 'html')
        message.attach(content)
        message['To'] = to_user
        message['From'] = env_config.GMAIL_USER
        message['Subject'] = Hardcode.EMAIL_SUBJECT.value
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message
        }
        
        headers = {'Authorization': f'Bearer {access_token}'}
        res = await post_request(env_config.GOOGLE_SENDING_EMAIL_API, headers=headers, json=create_message)
        if res.is_error:
            LogService.error(res.json())
            raise SCException(status.HTTP_503_SERVICE_UNAVAILABLE, ErrorCode.SC005)
    except SCException as e:
        LogService.error('Something went wrong while sending email')
    LogService.info('Sending email ends')
