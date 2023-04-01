from peewee_migrate import Router

from app.models import user, skin
from app.core.DataBase import db
from config.app import settings as AppConfig

def gen():
    with db:
        router = Router(db)
        router.create("user", auto=user.User)
        router.create("skin", auto=skin.Skin)


def run():
    with db:
        router = Router(db)
        router.run(AppConfig.BASE_PATH + '\\database\\migrations\\004_token.py')


if __name__ == "__main__":
    db.connect()

    run()

    db.close()
