from typing import Optional, Union, List

from pydantic import BaseModel

from app.schemas.player import Player
from app.schemas.user import User


class Base(BaseModel):
    class Config:
        orm_mode = True


class OAuth2PasswordRequest(Base):
    grant_type: Optional[str] = 'password'
    username: str
    password: str
    scope: Optional[str] = ''
    client_id: Optional[str] = None
    client_secret: Optional[str] = None


class LoginToken(Base):
    access_token: str
    token_type: str


class Agent(Base):
    name: str
    version: int


class TokenBase(Base):
    access_token: str
    client_token: str

    class Config:
        orm_mode = True


class TokenData(Base):
    username: Union[str, None] = None


class AuthBase(Base):
    username: str
    password: str

    class Config:
        orm_mode = True


class RefreshResponse(TokenBase):
    selectedProfile: Optional[Player] = None
    user: Optional[User] = None


class AuthResponse(RefreshResponse):
    availableProfiles: Optional[List[Player]] = None


class AuthRequest(AuthBase):
    client_token: Optional[str] = None
    request_user: Optional[bool] = False


class RefreshRequest(TokenBase):
    request_user: Optional[bool] = False
    selectedProfile: Player
