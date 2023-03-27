import datetime

from app.http.deps import get_db
from app.models.token import Token
from app.models.user import User
from app.services.auth import hashing

if __name__ == "__main__":
    get_db()
    password = hashing.get_password_hash("123456")
    tokens = Token.select().where(Token.user_id == 1)
    user = User.get_or_none(User.username == 'cnlimiter')

    # if tokens:
    #     print(True)
    # else:
    #     print(False)
    # for i in tokens:
    #     print(i.token_id)

    # print(user.password)
    print(datetime.datetime.utcnow().timestamp()-user.created_at)
    #for i in tokens:
