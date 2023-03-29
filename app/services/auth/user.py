import base64
import datetime

from app.models.skin import Skin
from app.models.user import User
from app.schemas.player import Player, Properties
from app.support.helper import gen_signed_date
from config.api import settings as ApiConfig


def gen_user_profile(user_data: User, properties_contained: bool = True):
    skin = Skin.get_or_none(Skin.uploader == user_data.user_id)
    if properties_contained:
        texture_data = {
            'timestamp': datetime.datetime.now(),
            'profileId': user_data.uuid,
            'profileName': user_data.username,
            'textures': {
                "SKIN": {
                    'url': f"{ApiConfig.URL}/textures/{skin.hash}",
                    'metadata': {
                        "model": "default" if skin.type == 0 else "slim"
                    }
                }
            }
        }

        texture_data = base64.b64encode(texture_data.__str__().encode('utf-8'))

        if properties_contained:
            data = Player(
                id=user_data.uuid,
                name=user_data.username,
                properties=[Properties(
                    name='textures',
                    value=texture_data,
                    signature=gen_signed_date(texture_data)
                )]
            )
        else:
            data = Player(
                id=user_data.uuid,
                name=user_data.username
            )

        return data
