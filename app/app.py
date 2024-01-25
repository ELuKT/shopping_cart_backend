#! /home/ericlu/workspace/fastapi-sc-backend/.venv/bin/python
import secrets
from fastapi import FastAPI
from app.config.common_middleware import CommonMiddleware
from app.config.sc_exception_handlers import sc_exception_handler
from app.config.settings import get_env_config
from app.config.uncatched_exception_handler import uncatched_exception_handler
from app.config.lifespan import lifespan
from app.model.common import SCException
from app.router import cart, auth, product, refresh, record, health
from starlette.middleware.sessions import SessionMiddleware


env_config = get_env_config()
app = FastAPI(lifespan=lifespan, docs_url=env_config.DOCS_URL, redoc_url=None)

urls = [
    ("cart", cart.router, "cart"),
    ("auth", auth.router, "auth"),
    ("product", product.router, "product"),
    ("refresh", refresh.router, "refresh"),
    ("record", record.router, "record"),
    ("health", health.router, "health")
]

for prefix, router, tag in urls:
    app.include_router(router=router, prefix=f"/v1/{prefix}", tags=[tag])

app.add_exception_handler(Exception, uncatched_exception_handler)
app.add_exception_handler(SCException, sc_exception_handler)
app.add_middleware(CommonMiddleware)
app.add_middleware(SessionMiddleware, secret_key=secrets.token_bytes(32))
