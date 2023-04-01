from fastapi import APIRouter

from app.support.key_helper import load_key
from config.api import settings as api_config

router = APIRouter(

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
