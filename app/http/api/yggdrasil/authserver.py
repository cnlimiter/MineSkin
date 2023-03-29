from fastapi import APIRouter, Depends

from app.http.deps import get_db
from app.schemas.auth import AuthRequest, AuthResponse, RefreshRequest, RefreshResponse, TokenBase, AuthBase
from app.services.yggdrasil.auth_service import Password, Refresh, Validate, InValidate, SignOut

router = APIRouter(
    prefix="/yggdrasil/authserver"
)


@router.post("/authenticate", response_model=AuthResponse, dependencies=[Depends(get_db)])
async def authenticate(request_data: AuthRequest = Depends()):
    """
    使用密码进行身份验证，并分配一个新的令牌。
    """
    r = Password(request_data)
    return r.respond()


@router.post("/refresh", response_model=RefreshResponse, dependencies=[Depends(get_db)])
async def refresh(request_data: RefreshRequest):
    """
    吊销原令牌，并颁发一个新的令牌。
    """
    r = Refresh(request_data)
    return r.respond()


@router.post("/validate", dependencies=[Depends(get_db)])
async def validate(request_data: TokenBase):
    """
    检验令牌是否有效。
    """
    r = Validate(request_data)
    return r.respond()


@router.post("/invalidate", dependencies=[Depends(get_db)])
async def invalidate(access_token: str):
    """
    检验令牌是否有效。
    """
    r = InValidate(access_token)
    return r.respond()


@router.post("/signout", dependencies=[Depends(get_db)])
async def signout(request_data: AuthBase):
    """
    吊销用户的所有令牌。
    """
    r = SignOut(request_data)
    return r.respond()
