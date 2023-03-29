from starlette.requests import Request
from starlette.responses import JSONResponse

from app.schemas.game import JoinRequest
from app.services.auth.token import client_to_server_validate,server_to_client_validate
from app.support.response_json import YggdrasilResponse


class Join:
    def __init__(self, data: JoinRequest, request: Request):
        self.data = data
        self.request = request

    def respond(self):
        r = self.data
        if not r.access_token or \
                not r.selectedProfile or \
                not r.serverId or \
                not len(r.access_token) == 32 or \
                not len(r.selectedProfile) == 32:
            return YggdrasilResponse.invalidToken()

        access_token = r.access_token
        selected_profile = r.selectedProfile
        server_id = r.serverId
        client_ip = self.request.client.host

        # 比对并储存数据
        result = client_to_server_validate(access_token, selected_profile, server_id, client_ip)

        # 操作失败，返回403
        if not result:
            return YggdrasilResponse.invalidToken()

        # 操作成功，返回204
        return YggdrasilResponse.noContent()


class HasJoined:
    def __init__(self, username: str, serverId: str, ip: str):
        self.username = username
        self.server_id = serverId
        self.ip = ip

    def respond(self):
        username = self.username
        server_id = self.server_id
        ip = self.ip

        # 比对授权 生成玩家信息
        result = server_to_client_validate(username, server_id, ip)

        # 操作失败，返回403
        if not result:
            return YggdrasilResponse.invalidToken()

        # 操作成功，返回204
        return YggdrasilResponse.noContent()
