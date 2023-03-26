from typing import List

from pydantic import BaseModel


class Properties(BaseModel):
    name: str
    value: str
    signature: str


class Player(BaseModel):
    id: str
    name: str
    properties: List[Properties]