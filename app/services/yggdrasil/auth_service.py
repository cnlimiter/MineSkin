from starlette.responses import JSONResponse

from app.exceptions.exception import InvalidCredentialsError, InvalidTokenError
from app.models.user import User
from app.schemas.auth import AuthRequest, AuthResponse, RefreshRequest, RefreshResponse, TokenBase, AuthBase
from app.schemas.player import Player as PlayerRes, Player
from app.schemas.user import User as UserRes
from app.services.yggdrasil import hashing as PwdService, token as TokenService
from app.services.util import hashing
from app.support.helper import numeric_random


class Password:
    def __init__(self, request_data: AuthRequest):
        self.request_data = request_data

    def respond(self) -> AuthResponse:
        user = User.get_or_none(User.username == self.request_data.username)
        if not user:
            raise InvalidCredentialsError(message='User not exist')
        password = self.request_data.password
        # 用户密码校验
        if not (user.password and PwdService.verify_password(password, user.password)):
            raise InvalidCredentialsError(message='Incorrect email or password')

        # 用户状态校验
        if not user.is_enabled():
            raise InvalidCredentialsError(message='Inactive user')

        if self.request_data.client_token is None:
            self.request_data.client_token = numeric_random()

        access_token = TokenService.gen_access_token(self.request_data.username, self.request_data.client_token)
        profile_data = PlayerRes(id=user.uuid, name=user.username)

        response_data = AuthResponse(access_token=access_token, client_token=self.request_data.client_token,
                                     availableProfiles=[profile_data]
                                     )

        response_data.selectedProfile = profile_data

        if self.request_data.request_user:
            s_user = UserRes(id=user.uuid)
            response_data.user = s_user

        return response_data


class Refresh:
    def __init__(self, request_data: RefreshRequest):
        self.request_data = request_data

    def respond(self) -> RefreshResponse:
        if not self.request_data.access_token:
            raise InvalidTokenError(message='未知的令牌')
        access_token = self.request_data.access_token
        client_token = self.request_data.client_token
        request_user = self.request_data.request_user
        """刷新令牌"""
        token = TokenService.refresh_access_token(access_token=access_token, client_token=client_token)
        if not token:
            raise InvalidTokenError(message='未知的令牌')

        profile_data = Player(id=token.get("uuid"), name=token.get("playername"))

        response_data = RefreshResponse(access_token=token.get("access_token"), client_token=token.get("client_token"))

        response_data.selectedProfile = profile_data

        if request_user:
            r_user = UserRes(id=token.get("uuid"))
            response_data.user = r_user

        return response_data


class Validate:
    def __init__(self, request_data: TokenBase):
        self.request_data = request_data

    def respond(self):
        # 属性accessToken不存在
        if not self.request_data.access_token:
            raise InvalidTokenError()
        access_token = self.request_data.access_token
        client_token = self.request_data.client_token

        # 验证令牌
        token = TokenService.validate_access_token(access_token=access_token, client_token=client_token)

        # 验证失败或令牌无效
        if not token:
            raise InvalidTokenError()

        # 令牌有效，返回204
        return JSONResponse(status_code=204, content={})


class InValidate:
    def __init__(self, access_token: str):
        self.access_token = access_token

    def respond(self):
        # 属性accessToken不存在
        if self.access_token:
            TokenService.invalidate_access_token(self.access_token)

        # 令牌有效，返回204
        return JSONResponse(status_code=204, content={})


class SignOut:
    def __init__(self, data: AuthBase):
        self.data = data

    def respond(self):

        # 属性accessToken不存在
        if not self.data.username or not self.data.password:
            raise InvalidCredentialsError()

        username = self.data.username
        password = hashing.get_password_hash(self.data.password)

        result = TokenService.invalidate_all_access_token(username=username, password=password)

        if not result:
            raise InvalidCredentialsError()

        # 令牌有效，返回204
        return JSONResponse(status_code=204, content={})
