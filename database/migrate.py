from peewee_migrate import Router

import config.config
from app.models import user, skin, player
from app.providers.database import db


def gen():
    with db:
        router = Router(db)
        router.create("user", auto=user.User)
        router.create("player", auto=player.Player)
        router.create("skin", auto=skin.Skin)


def run():
    with db:
        router = Router(db)
        router.run(config.config.settings.BASE_PATH + '\\database\\migrations\\001_user.py')


if __name__ == "__main__":
    db.connect()

    run()

    db.close()
