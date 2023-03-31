"""
框架异常类
"""


class InvalidToken(Exception):
    """
    未认证
    """

    def __init__(self, message: str = "Invalid token."):
        self.type = 'ForbiddenOperationException'
        self.message = message


class NoContent(Exception):
    """
    未授权
    """


class Forbidden(Exception):
    """
    未授权
    """

    def __init__(self, message: str):
        self.type = 'ForbiddenOperationException'
        self.message = message


class InvalidCredentials(Exception):
    """
    已经出现
    """

    def __init__(self, message: str = "Invalid credentials. Invalid username or password."):
        self.type = 'ForbiddenOperationException'
        self.message = message
