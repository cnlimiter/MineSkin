from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.http.deps import get_db
from app.schemas.game import JoinRequest
from app.services.auth.session_service import Join, HasJoined

router = APIRouter(
    prefix="/yggdrasil/sessionserver/session/minecraft"
)


@router.post("/join", dependencies=[Depends(get_db)])
async def authenticate(request: Request, request_data: JoinRequest = Depends()):
    """
    客户端进入服务器。
    """
    r = Join(request_data, request)
    return r.respond()


@router.get("/hasJoined/", dependencies=[Depends(get_db)])
async def authenticate(username: str, serverId: str, ip: str):
    """
    客户端进入服务器。
    """
    r = HasJoined(username, serverId, ip)
    return r.respond()
