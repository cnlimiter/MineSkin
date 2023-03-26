from starlette.responses import JSONResponse

from app.exceptions.exception import AuthenticationError, AuthorizationError
from app.models.user import User
from app.schemas.authenticate import AuthRequest, AuthResponse, RefreshRequest, RefreshResponse, TokenBase
from app.schemas.player import Player as PlayerRes, Player
from app.schemas.user import User as UserRes, ProfileData
from app.services.auth import hashing as PwdService, token as TokenService


class Password:
    def __init__(self, request_data: AuthRequest):
        self.request_data = request_data

    def respond(self) -> AuthResponse:
        user = User.get_or_none(User.username == self.request_data.username)
        if not user:
            raise AuthenticationError(message='User not exist')

        # 用户密码校验
        if not (user.password and PwdService.verify_password(self.request_data.password, user.password)):
            raise AuthenticationError(message='Incorrect email or password')

        # 用户状态校验
        if not user.is_enabled():
            raise AuthenticationError(message='Inactive user')

        access_token = TokenService.gen_access_token(self.request_data.username, self.request_data.client_token)
        profile_data = PlayerRes()
        profile_data.id = user.uuid
        profile_data.name = user.username

        response_data = AuthResponse()
        response_data.access_token = access_token
        response_data.client_token = self.request_data.client_token
        response_data.availableProfiles.append(profile_data)
        response_data.selectedProfile = profile_data

        if self.request_data.request_user:
            s_user = UserRes()
            s_user.id = user.uuid
            response_data.user = s_user

        return response_data


class Refresh:
    def __init__(self, request_data: RefreshRequest):
        self.request_data = request_data

    def respond(self) -> RefreshResponse:
        if not self.request_data.access_token:
            raise AuthorizationError(message='未知的令牌')
        access_token = self.request_data.access_token
        client_token = self.request_data.client_token
        request_user = self.request_data.request_user
        """刷新令牌"""
        token = TokenService.refresh_access_token(access_token=access_token, client_token=client_token)
        if not token:
            raise AuthenticationError(message='未知的令牌')

        profile_data = Player()
        profile_data.id = token.get("uuid")
        profile_data.name = token.get("playername")

        response_data = RefreshResponse()
        response_data.access_token = token.get("access_token")
        response_data.client_token = token.get("client_token")
        response_data.selectedProfile = profile_data

        if request_user:
            r_user = UserRes()
            r_user.id = token.get("uuid")
            response_data.user = r_user

        return response_data


class Validate:
    def __init__(self, request_data: TokenBase):
        self.request_data = request_data

    def respond(self):
        # 属性accessToken不存在
        if not self.request_data.access_token:
            raise AuthorizationError(message='未知的令牌')
        access_token = self.request_data.access_token
        client_token = self.request_data.client_token

        # 验证令牌
        token = TokenService.validate_access_token(access_token=access_token, client_token=client_token)

        # 验证失败或令牌无效
        if not token:
            raise AuthenticationError(message='未知的令牌')

        # 令牌有效，返回204
        return JSONResponse(status_code=204, content={})
