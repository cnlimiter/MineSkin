import datetime
import uuid
from typing import List

from app.exceptions.exception import AuthenticationError
from app.models.token import Token
from app.models.user import User
from app.schemas.auth import TokenBase


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
        raise AuthenticationError(message="用户已封禁或不存在")


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
            raise AuthenticationError(message='用户已封禁或不存在')


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


def client_to_server_validate(access_token: str, selected_profile: str, server_id: str, ip: str):
    token: Token = Token.get_or_none(Token.access_token == access_token)
    user: User = User.get_by_id(token.user_id)

    if not user:
        return False

    if user.permission == 1:
        return False

