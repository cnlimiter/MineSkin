import datetime
import json

from app.http.deps import get_db
from app.models.token import Token
from app.models.user import User
from app.schemas.texture import Texture, SkinInfo
from app.support import hashing
from app.support.response_helper import YggdrasilResponse

if __name__ == "__main__":
    get_db()
    password = hashing.get_password_hash("123456")
    tokens = Token.select().where(Token.user_id == 2)
    token = Token.get_or_none(Token.token_id == 2)
    user = User.get_or_none(User.username == 'cnlimiter')

    result = hashing.verify_password('123456', user.password)

    now = datetime.datetime.now().timestamp()

    data = {
        'access_token': '1',
        'selected_profile': '1',
        'username': '1',
        'ip': '1'
    }
    dump = json.dumps(data)

    texture = SkinInfo(
        url="111",
        metadata={
            'model': 'default'
        }
    )

    texture_data = Texture(
        timestamp=datetime.datetime.now(),
        profileId='1',
        profileName='1',
        textures={
            "SKIN": texture
        }
    )


    # if tokens:
    #     print(True)
    # else:
    #     print(False)
    # for i in tokens:
    #     print(i.token_id)
    # print(base64.b64encode(data.__str__().encode('utf-8')))

    #print(convert_uuid_with_hyphen(uuid.uuid4().hex))

    # print(token.created_at.timestamp())
    # print(datetime.datetime.utcnow().timestamp()-user.created_at)



    print(YggdrasilResponse.success("test").render())