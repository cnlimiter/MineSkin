from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError
from jose.exceptions import JWTClaimsError

from app.exceptions.exception import AuthenticationError
from app.models.user import User
from app.providers import database
from app.services.auth import jwt_helper

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
