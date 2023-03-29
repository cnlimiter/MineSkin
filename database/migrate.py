from peewee_migrate import Router

from app.models import user, skin, player, token
from app.providers.database import db
from config import app


def gen():
    with db:
        router = Router(db)
        router.create("user", auto=user.User)
        router.create("player", auto=player.Player)
        router.create("skin", auto=skin.Skin)


def run():
    with db:
        router = Router(db)
        router.run(config.settings.BASE_PATH + '\\database\\migrations\\004_token.py')


if __name__ == "__main__":
    db.connect()

    run()

    db.close()
