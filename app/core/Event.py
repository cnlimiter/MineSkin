from fastapi.middleware.cors import CORSMiddleware
from redis.client import Redis

from app.core.DataBase import db, sys_cache, code_cache
from config.app import settings


def register(app):
    app.debug = settings.DEBUG
    app.title = settings.NAME

    add_global_middleware(app)

    @app.on_event("startup")
    def startup():
        db.connect()

        app.state.cache = sys_cache()
        app.state.code_cache = code_cache()

    @app.on_event("shutdown")
    def shutdown():
        if not db.is_closed():
            db.close()
        cache: Redis = app.state.cache
        code: Redis = app.state.code_cache
        cache.close()
        code.close()


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
