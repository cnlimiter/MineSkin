from fastapi import APIRouter, Depends

from app.http.deps import get_db
from app.schemas.game import JoinRequest

router = APIRouter(
    prefix="/yggdrasil/sessionserver/session/minecraft"
)


@router.post("/join", response_model=AuthResponse, dependencies=[Depends(get_db)])
async def authenticate(request_data: JoinRequest = Depends()):
    """
    使用密码进行身份验证，并分配一个新的令牌。
    """
    r = Password(request_data)
    return r.respond()
