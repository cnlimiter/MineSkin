from typing import Optional, Union, List

from pydantic import BaseModel
from user import User
from player import Player


class Agent(BaseModel):
    name: str
    version: int


class TokenBase(BaseModel):
    access_token: str
    client_token: str


class AuthBase(BaseModel):
    username: str
    password: str


class RefreshResponse(TokenBase):
    selectedProfile: Player
    user: User


class AuthResponse(RefreshResponse):
    availableProfiles: List[Player]


class AuthRequest(AuthBase):
    client_token: Optional[str] = None
    request_user: Optional[bool] = False


class RefreshRequest(TokenBase):
    request_user: Optional[bool] = False
    selectedProfile: Player
