import logging

from fastapi import FastAPI

from app.core import Event, Router, Exception, Logging


def create_app() -> FastAPI:
    logging.info("App initializing")

    app = FastAPI()

    register(app, Event)
    register(app, Logging)
    register(app, Exception)

    boot(app, Router)

    return app


def register(app, provider):
    logging.info(provider.__name__ + ' registering')
    provider.register(app)


def boot(app, provider):
    logging.info(provider.__name__ + ' booting')
    provider.boot(app)
