from fastapi import APIRouter

from app.http.controller.api.yggdrasil import authserver
from app.http.controller.api.yggdrasil import sessionserver
from app.http.controller.common import users
from app.http.controller.api import yggdrasil

yggdrasil_router = APIRouter()

api_router = APIRouter()

yggdrasil_router.include_router(yggdrasil.router, tags=["yggdrasil"], prefix="/yggdrasil")

yggdrasil_router.include_router(authserver.router, tags=["yggdrasil.yggdrasil"], prefix="/yggdrasil")

yggdrasil_router.include_router(sessionserver.router, tags=["yggdrasil.game"], prefix="/yggdrasil")

api_router.include_router(users.router, tags=["user"])
