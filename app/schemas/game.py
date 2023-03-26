from pydantic import BaseModel


class JoinRequest(BaseModel):
    access_token: str
    selectedProfile: str
    serverId: str

