from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.support.helper import load_key
from config.api import settings as api_config

from fastapi import APIRouter, Depends

from app.http.deps import get_db
from app.schemas.auth import AuthRequest, AuthResponse, RefreshRequest, RefreshResponse, TokenBase, AuthBase
from app.services.auth.grant import Password, Refresh, Validate, InValidate, SignOut

router = APIRouter(
    prefix="/yggdrasil"
)


@router.get("/")
def main():
    """
    元消息
    """
    return {
        "meta": {
            "implementationName": api_config.API_NAME,
            "implementationVersion": api_config.VERSION,
            "serverName": api_config.SERVER_NAME,
            "links": {
                "homepage": api_config.URL,
                "register": api_config.URL + "/register"
            },
            "feature.non_email_login": True
        },
        "skinDomains": api_config.DOMAINS,
        "signaturePublickey": load_key()
    }


@router.post("/authserver/authenticate", response_model=AuthResponse, dependencies=[Depends(get_db)])
async def authenticate(request_data: AuthRequest= Depends()):
    """
    使用密码进行身份验证，并分配一个新的令牌。
    """
    r = Password(request_data)
    return r.respond()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    data = form_data
    print(data.username)
    print(data.password)
    for scope in data.scopes:
        print(scope)
    if data.client_id:
        print(data.client_id)
    if data.client_secret:
        print(data.client_secret)
    return data

@router.post("/authserver/refresh", response_model=RefreshResponse, dependencies=[Depends(get_db)])
async def refresh(request_data: RefreshRequest):
    """
    吊销原令牌，并颁发一个新的令牌。
    """
    r = Refresh(request_data)
    return r.respond()


@router.post("/authserver/validate", dependencies=[Depends(get_db)])
async def validate(request_data: TokenBase):
    """
    检验令牌是否有效。
    """
    r = Validate(request_data)
    return r.respond()


@router.post("/authserver/invalidate", dependencies=[Depends(get_db)])
async def invalidate(access_token: str):
    """
    检验令牌是否有效。
    """
    r = InValidate(access_token)
    return r.respond()


@router.post("/authserver/signout", dependencies=[Depends(get_db)])
async def signout(request_data: AuthBase):
    """
    吊销用户的所有令牌。
    """
    r = SignOut(request_data)
    return r.respond()
