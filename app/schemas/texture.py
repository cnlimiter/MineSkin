import datetime
from typing import Union

from pydantic import BaseModel


class SkinInfo(BaseModel):
    url: str
    metadata: dict[str, str]


class Texture(BaseModel):
    timestamp: datetime.datetime
    profileId: str
    profileName: str
    textures: dict[str, SkinInfo]
