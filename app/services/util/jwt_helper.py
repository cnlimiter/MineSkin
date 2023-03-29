from datetime import datetime, timedelta

from jose import jwt
from typing import Any, Union

from config.jwt import settings


def create_access_token(
        data: dict, expires_delta: Union[timedelta, None] = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.TTL)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_payload_by_token(encoded_jwt):
    return jwt.decode(encoded_jwt, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
