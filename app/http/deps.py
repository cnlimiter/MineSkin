from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError
from jose.exceptions import JWTClaimsError
from starlette import status

from app.exceptions.exception import AuthenticationError
from app.models.user import User
from app.providers import database
from app.schemas.auth import TokenData, AuthRequest
from app.services.util import jwt_helper

oauth2_token_schema = OAuth2PasswordBearer(
    tokenUrl="token"
)


def get_auth_user(
        token: str = Depends(oauth2_token_schema)
) -> User:
    try:
        payload = jwt_helper.get_payload_by_token(token)
    except ExpiredSignatureError:
        raise AuthenticationError(message="Token Expired")
    except (JWTError, JWTClaimsError):
        raise AuthenticationError(message="Could not validate credentials")

    user_id = payload.get('sub')
    user = User.get_or_none(User.user_id == user_id)

    if not user:
        raise AuthenticationError(message="User not found")
    if not user.is_enabled():
        raise AuthenticationError(message='Inactive user')
    return user


def get_db():
    try:
        database.db.connect()
        yield
    finally:
        if not database.db.is_closed():
            database.db.close()


from app.services.util.hashing import verify_password
from app.services.util.jwt_helper import get_payload_by_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authserver/authenticate")


def authenticate_user(username: str, password: str):
    # This doesn't provide any security at all
    # Check the next version
    user = User.get_or_none(User.username, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = get_payload_by_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = User.get_or_none(User.username, username=token_data.username)
    if user is None:
        raise credentials_exception
    c_user = AuthRequest()
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
