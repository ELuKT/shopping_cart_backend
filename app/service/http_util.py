from httpx import Response
from app.config.lifespan import httpx_client
from app.model.common.enums import ErrorCode
from app.model.common.sc_exception import SCException
from fastapi import status

async def post_request(req_url, headers, param=None, json=None)->Response:
    # Opening and closing clients: https://www.python-httpx.org/async/
    if not httpx_client:
        raise SCException(status.HTTP_503_SERVICE_UNAVAILABLE, ErrorCode.SC005)
    return await httpx_client.post(req_url, headers=headers, params=param, json=json)
