from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.model.common.sc_exception import SCException
from app.model.entity.custom_exception import CustomException
from app.service.log_service import LogService
from .redis_cache import RedisCache


async def sc_exception_handler(request: Request, e: SCException):
    LogService.error(e)

    custom_exception = await RedisCache.get_cache(e.error_code, CustomException)
    if not custom_exception:
        custom_exception = await CustomException.find_one(CustomException.error_code == e.error_code)
        if custom_exception:
            await RedisCache.set_cache(e.error_code, custom_exception)
        else:
            LogService.error(f'Can not found {e.error_code} exception in DB')
            return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content='System busy, please try again later')
    LogService.error(custom_exception.description)
    return JSONResponse(
        status_code=e.status_code, content={"message":custom_exception.description},
    )
