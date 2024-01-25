from contextvars import ContextVar
import logging
from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.service.common import generate_request_id

REQUEST_ID_CTX_KEY = "REQUEST_ID_CTX_KEY"
_request_id_ctx_var: ContextVar[str] = ContextVar(REQUEST_ID_CTX_KEY, default=None)

def get_request_id() -> str:
    return _request_id_ctx_var.get()

class CommonMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if not _request_id_ctx_var.get():
            _request_id_ctx_var.set(generate_request_id())
            logging.info(f"set session id: {get_request_id()} to context")

        response = await call_next(request)

        return response
