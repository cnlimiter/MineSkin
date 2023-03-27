from fastapi import APIRouter

from app.http.api import demo, yggdrasil, users

api_router = APIRouter()

api_router.include_router(demo.router, tags=["demo"])

api_router.include_router(users.router, tags=["users"])

api_router.include_router(yggdrasil.router, tags=["yggdrasil"])
