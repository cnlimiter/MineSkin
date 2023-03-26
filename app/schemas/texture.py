import datetime
from typing import Union

from pydantic import BaseModel


class SkinInfo(BaseModel):
    url: str
    metadata: Union[str, str]


class Texture(BaseModel):
    timestamp: datetime.datetime
    profileId: str
    profileName: str
    textures: Union[str, SkinInfo]
