from typing import List, Optional

from pydantic import BaseModel


class Properties(BaseModel):
    name: str
    value: str


class User(BaseModel):
    id: str
    properties: Optional[List[Properties]] = None


class ProfileData(BaseModel):
    id: str
    name: str
