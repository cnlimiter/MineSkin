"""
框架异常类
"""
from fastapi.exception_handlers import request_validation_exception_handler, http_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import Request


class LoginError(Exception):
    """
    未认证
    """

    def __init__(self, message: str = ""):
        self.message = message


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


def register(app):
    @app.exception_handler(LoginError)
    async def invalidToken(request: Request, e: LoginError):
        """
        认证异常处理
        """
        return JSONResponse(content={
            "code": -1,
            "msg": e.message
        })

    @app.exception_handler(InvalidToken)
    async def invalidToken(request: Request, e: InvalidToken):
        """
        认证异常处理
        """
        return JSONResponse(status_code=403, content={
            "error": e.type,
            "errorMessage": e.message
        })

    @app.exception_handler(NoContent)
    async def noContent(request: Request):
        """
        权限异常处理
        """
        return JSONResponse(status_code=204, content={})

    @app.exception_handler(Forbidden)
    async def forbidden(request: Request, e: Forbidden):
        """
        重复异常处理
        """
        return JSONResponse(status_code=403, content={
            "error": e.type,
            "errorMessage": e.message
        })

    @app.exception_handler(InvalidCredentials)
    async def invalidCredentials(request: Request, e: InvalidCredentials):
        """
        重复异常处理
        """
        return JSONResponse(status_code=403, content={
            "error": e.type,
            "errorMessage": e.message
        })

    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request: Request, exc):
        return await http_exception_handler(request, exc)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc):
        return await request_validation_exception_handler(request, exc)
