from typing import List

from pydantic import BaseModel


class Properties(BaseModel):
    name: str
    value: str


class User(BaseModel):
    id: str
    properties: List[Properties]


class ProfileData(BaseModel):
    id: str
    name: str
