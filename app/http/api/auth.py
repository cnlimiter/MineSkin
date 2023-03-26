from fastapi import APIRouter, Depends

from app.http.deps import get_db
from app.schemas.authenticate import AuthRequest, AuthResponse, RefreshRequest, RefreshResponse, TokenBase
from app.services.auth.grant import Password, Refresh, Validate

router = APIRouter(
    prefix="/authserver"
)


@router.post("/authenticate", response_model=AuthResponse, dependencies=[Depends(get_db)])
async def token(request_data: AuthRequest):
    """
    使用密码进行身份验证，并分配一个新的令牌。
    """
    r = Password(request_data)
    return r.respond()


@router.post("/refresh", response_model=RefreshResponse, dependencies=[Depends(get_db)])
async def token(request_data: RefreshRequest):
    """
    吊销原令牌，并颁发一个新的令牌。
    """
    r = Refresh(request_data)
    return r.respond()


@router.post("/validate", dependencies=[Depends(get_db)])
async def token(request_data: TokenBase):
    """
    检验令牌是否有效。
    """
    r = Validate(request_data)
    return r.respond()
