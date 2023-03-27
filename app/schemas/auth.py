from typing import Optional, Union, List

from pydantic import BaseModel

from app.schemas.player import Player
from app.schemas.user import User


class Agent(BaseModel):
    name: str
    version: int

    class Config:
        orm_mode = True


class TokenBase(BaseModel):
    access_token: str
    client_token: str

    class Config:
        orm_mode = True


class AuthBase(BaseModel):
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
