from aioredis import Redis
from fastapi.middleware.cors import CORSMiddleware

from app.core.DataBase import db, sys_cache, code_cache
from config.app import settings


def register(app):
    app.debug = settings.DEBUG
    app.title = settings.NAME

    add_global_middleware(app)

    @app.on_event("startup")
    def startup():
        db.connect()

        app.state.cache = await sys_cache()
        app.state.code_cache = await code_cache()

    @app.on_event("shutdown")
    def shutdown():
        if not db.is_closed():
            db.close()
        cache: Redis = await app.state.cache
        code: Redis = await app.state.code_cache
        await cache.close()
        await code.close()


def add_global_middleware(app):
    """
    注册全局中间件
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
