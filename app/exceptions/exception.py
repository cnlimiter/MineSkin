"""
框架异常类
"""


class AuthenticationError(Exception):
    """
    未认证
    """

    def __init__(self, message: str = "Unauthorized"):
        self.message = message


class AuthorizationError(Exception):
    """
    未授权
    """

    def __init__(self, message: str = "Forbidden"):
        self.message = message


class ExistError(Exception):
    """
    已经出现
    """

    def __init__(self, message: str = "Exist"):
        self.message = message
