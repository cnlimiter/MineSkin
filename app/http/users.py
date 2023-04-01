from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import JSONResponse

from app.exceptions.exception import LoginError
from app.http.deps import get_db, authenticate_user, get_current_user
from app.models.user import User
from app.schemas.auth import LoginToken
from app.support.jwt_helper import create_access_token
from config.jwt import settings as JWTConfig

router = APIRouter(
)


@router.get("/")
async def root():
    return "Welcome!"


@router.post("/login", response_model=LoginToken, dependencies=[Depends(get_db)])
def me(auth_user: OAuth2PasswordRequestForm = Depends()):
    """
    登录
    """

    user = authenticate_user(auth_user.username, auth_user.password)
    if not user:
        raise LoginError("用户不存在或密码错误")
    access_token_expires = timedelta(minutes=JWTConfig.TTL)
    return LoginToken(
        access_token=create_access_token(user.user_id, expires_delta=access_token_expires),
        token_type="bearer"
    )


@router.get('/login/getinfo', dependencies=[Depends(get_db)])
def login_getinfo(
        current_user: User = Depends(get_current_user)
):
    data = {
        'username': current_user.username,
        'roles': ['admin', ]
    }
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)
