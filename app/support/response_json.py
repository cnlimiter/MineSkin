from starlette.responses import JSONResponse


class YggdrasilResponse:
    @staticmethod
    def invalidToken():
        return JSONResponse(
            status_code=403,
            content={
                'error': 'ForbiddenOperationException',
                'errorMessage': 'Invalid token.'
            }
        )

    @staticmethod
    def noContent():
        return JSONResponse(
            status_code=204,
        )

    @staticmethod
    def success(error: str, message: str):
        return JSONResponse(
            status_code=200,
            content={
                'error': error,
                'errorMessage': message
            }
        )

    @staticmethod
    def forbidden(message: str):
        return JSONResponse(
            status_code=403,
            content={
                'error': 'ForbiddenOperationException',
                'errorMessage': message
            }
        )

    @staticmethod
    def invalidCredentials():
        return JSONResponse(
            status_code=403,
            content={
                'error': 'ForbiddenOperationException',
                'errorMessage': 'Invalid credentials. Invalid username or password.'
            }
        )
