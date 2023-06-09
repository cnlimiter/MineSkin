import datetime
import json
import uuid
from typing import List

from redis.client import Redis
from starlette.requests import Request

from app.core.Exception import Forbidden
from app.models.token import Token
from app.models.user import User
from app.schemas.auth import TokenBase
from app.schemas.player import Player
from app.services.yggdrasil.user_profile import gen_user_profile
from config.auth import settings as AuthConfig


def gen_access_token(username: str, client_token: str) -> str:
    user = User.get_or_none(User.username == username)
    if user and user.permission != -1:
        tokens: List[Token] = Token.select().where(Token.user_id == user.user_id)

        for i in tokens:
            i.status = 0

        for i in tokens:
            if datetime.datetime.utcnow().timestamp() - i.created_at.timestamp() >= 432000000:
                Token.delete_by_id(i.token_id)

        new_token = TokenBase(access_token=uuid.uuid4().hex, client_token=client_token)
        # new_token.access_token = uuid.uuid4().hex
        # new_token.client_token = client_token
        Token.create(user_id=user.user_id, client_token=new_token.client_token, access_token=new_token.access_token)
        return new_token.access_token
    else:
        raise Forbidden(message="用户已封禁或不存在")


def search_user_by_access_token(access_token: str) -> User:
    token = Token.get_or_none(access_token=access_token)
    return User.get_by_id(token.user_id)


def refresh_access_token(access_token: str, client_token: str):
    token: Token
    tokens: List[Token] = Token.select().where(Token.access_token == access_token)
    for i in tokens:
        user: User = User.get_by_id(i.user_id)
        if user and user.permission != -1:
            if datetime.datetime.utcnow().timestamp() - i.created_at >= 432000000:
                Token.delete_by_id(i.token_id)
                break
            if not i.access_token == access_token:
                break

            if not i.client_token == client_token:
                break

            token = i
            token.status = 1

            return {
                "accessToken": token.access_token,
                "clientToken": token.clientToken,
                "uuid": user.uuid,
                "playername": user.username
            }

        else:
            raise Forbidden(message='用户已封禁或不存在')


def validate_access_token(access_token: str, client_token: str) -> bool:
    tokens: List[Token] = Token.select().where(Token.access_token == access_token)
    for i in tokens:
        user: User = User.get_by_id(i.user_id)
        if user and user.permission != -1:
            # accessToken已过期
            if datetime.datetime.utcnow().timestamp() - i.created_at >= 432000000:
                Token.delete_by_id(i.token_id)
                break

            # 未找到指定accessToken
            if not i.access_token:
                break

            if not i.access_token == access_token:
                break

            # clientToken不匹配
            if not i.client_token == client_token:
                break
            # accessToken暂时失效
            if not i.status == 1:
                break

            return True

        else:
            return False

    return False


def invalidate_access_token(access_token: str) -> bool:
    token: Token = Token.get_or_none(Token.access_token == access_token)
    user: User = User.get_by_id(token.user_id)
    if user and user.permission != -1:
        if not token.access_token:
            return False
        Token.delete_by_id(token.token_id)
        return True
    return False


def invalidate_all_access_token(username: str, password: str) -> bool:
    user: User = User.get_or_none(User.username == username)
    if user and user.permission != -1:
        tokens: List[Token] = Token.select().where(Token.user_id == user.user_id)
        # 密码不正确
        if not password == user.password:
            return False

        # 遍历所有token并删除
        for i in tokens:
            Token.delete_by_id(i.token_id)

        return True
    else:
        return False


def client_to_server_validate(req: Request, access_token: str, selected_profile: str, server_id: str, ip: str) -> bool:
    redis: Redis = req.app.state.code_cache
    token: Token = Token.get_or_none(Token.access_token == access_token)
    user: User = User.get_by_id(token.user_id)

    if not user:
        return False

    # 令牌对应用户已被封禁
    if user.permission == -1:
        return False

    if not AuthConfig.EMAIL_IGNORE:
        # 令牌对应用户未验证邮箱
        if user.permission == 0:
            return False

    # 令牌对应玩家uuid不一致
    if user.uuid != selected_profile:
        return False

    data = {
        "access_token": access_token,
        "selected_profile": selected_profile,
        "username": user.username,
        "ip": ip
    }

    # 将授权信息储存至redis，15秒过期
    return redis.set(f'server_id_{server_id}', json.dumps(data), ex=15)


def server_to_client_validate(req: Request, username: str, server_id: str, ip: str) -> bool | Player:
    redis: Redis = req.app.state.code_cache
    # 根据serverId获取对应授权信息
    response = redis.get(f'server_id_{server_id}')
    # 未找到对应授权信息或发生错误
    if not response:
        return False
    client_data: dict[str, str] = json.loads(response)

    # 玩家名称与授权不对应
    if not client_data.get('username') == username:
        return False
    # 若提供了客户端ip，则需要判断储存的客户端ip与其是否一致
    if ip:
        if not client_data.get('ip') == ip:
            return False

    # 根据accessToken获取玩家资料
    user = search_user_by_access_token(client_data.get('access_token'))

    return gen_user_profile(user_data=user)
