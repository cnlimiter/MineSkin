from starlette.requests import Request

from app.core.Exception import InvalidToken
from app.models.user import User
from app.schemas.game import JoinRequest
from app.schemas.player import Player
from app.services.yggdrasil.auth_token import client_to_server_validate, server_to_client_validate
from app.core.Response import noContent


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
            raise InvalidToken()

        access_token = r.access_token
        selected_profile = r.selectedProfile
        server_id = r.serverId
        client_ip = self.request.client.host

        # 比对并储存数据
        result = client_to_server_validate(self.request, access_token, selected_profile, server_id, client_ip)

        # 操作失败，返回403
        if not result:
            raise InvalidToken()

        # 操作成功，返回204
        return noContent()


class HasJoined:
    def __init__(self, username: str, serverId: str, ip: str, req: Request):
        self.username = username
        self.server_id = serverId
        self.ip = ip
        self.req = req

    def respond(self):
        username = self.username
        server_id = self.server_id
        ip = self.ip

        # 比对授权 生成玩家信息
        result = server_to_client_validate(self.req, username, server_id, ip)

        # 操作失败，返回403
        if not result:
            return InvalidToken()

        # 操作成功，返回204
        return noContent()


class Profile:
    def __init__(self, uuid: str):
        self.uuid = uuid

    def respond(self):
        uuid = self.uuid

        # uuid格式错误，返回204
        if not len(uuid) == 32:
            return YggdrasilResponse.noContent()

        # # 处理无符号uuid为有符号uuid
        # t_uuid = convert_uuid_with_hyphen(uuid)

        # 根据UUID获取玩家信息
        user_data: User = User.get_or_none(User.uuid == uuid)
        player = Player(id=user_data.uuid, name=user_data.uuid)

        # 玩家不存在，返回204
        if not user_data:
            YggdrasilResponse.noContent()

        # 操作成功，返回204
        return player
