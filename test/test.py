import datetime

from app.http.deps import get_db
from app.models.token import Token
from app.models.user import User
from app.services.auth import hashing

if __name__ == "__main__":
    get_db()
    password = hashing.get_password_hash("123456")
    tokens = Token.select().where(Token.user_id == 2)
    token = Token.get_or_none(Token.token_id == 2)
    user = User.get_or_none(User.username == 'cnlimiter')

    result = hashing.verify_password('123456', user.password)

    now = datetime.datetime.now().timestamp()
    # if tokens:
    #     print(True)
    # else:
    #     print(False)
    # for i in tokens:
    #     print(i.token_id)
    print(now)

    print(token.created_at.timestamp())
    #print(datetime.datetime.utcnow().timestamp()-user.created_at)
    #for i in tokens:
