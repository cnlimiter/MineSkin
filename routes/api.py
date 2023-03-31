from fastapi import APIRouter

from app.http.api import yggdrasil
from app.http.api.yggdrasil import authserver, sessionserver
from app.http import users

yggdrasil_router = APIRouter()

api_router = APIRouter()

yggdrasil_router.include_router(yggdrasil.router, tags=["yggdrasil"], prefix="/yggdrasil")

yggdrasil_router.include_router(authserver.router, tags=["yggdrasil.yggdrasil"], prefix="/yggdrasil")

yggdrasil_router.include_router(sessionserver.router, tags=["yggdrasil.game"], prefix="/yggdrasil")

api_router.include_router(users.router, tags=["user"])
