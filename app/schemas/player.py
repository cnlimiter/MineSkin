from typing import List, Optional

from pydantic import BaseModel


class Properties(BaseModel):
    name: str
    value: str
    signature: str


class Player(BaseModel):
    id: str
    name: str
    properties: Optional[List[Properties]] = None

    class Config:
        orm_mode = True
