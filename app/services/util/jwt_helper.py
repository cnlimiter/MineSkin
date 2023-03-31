from datetime import datetime, timedelta

from jose import jwt
from typing import Any, Union

from config.jwt import settings as JWTConfig


def create_access_token(
        subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=JWTConfig.TTL
        )
    to_encode = {
        'exp': expire,
        'sub': str(subject)
    }
    encoded_jwt = jwt.encode(
        to_encode, JWTConfig.SECRET_KEY, algorithm=JWTConfig.ALGORITHM
    )
    return encoded_jwt


def get_payload_by_token(encoded_jwt):
    return jwt.decode(encoded_jwt, JWTConfig.SECRET_KEY, algorithms=JWTConfig.ALGORITHM)
