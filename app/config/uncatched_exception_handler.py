from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.service.log_service import LogService


async def uncatched_exception_handler(request: Request, e: Exception):
    LogService.error(e)
    return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content='System busy, please try again later')
