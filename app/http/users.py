from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.http.deps import get_db
from app.models.user import User
from app.schemas.auth import LoginToken

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

    user = User.get_or_none(User.email == auth_user.username)
    if not user:
        raise
    return auth_user
