from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from starlette import status

from app.models.user import User
from app.core.DataBase import db
from app.utils.hashing import verify_password
from app.core.Auth import get_payload_by_token

oauth2_token_schema = OAuth2PasswordBearer(
    tokenUrl="/login/"
)


def get_db():
    try:
        db.connect()
        yield
    finally:
        if not db.is_closed():
            db.close()



async def get_current_user(token: str = Depends(oauth2_token_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = get_payload_by_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = User.get_by_id(int(user_id))
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_enabled():
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
