from peewee import UUIDField, CharField, ForeignKeyField, AutoField

from app.models import user, skin
from app.models.base_model import BaseModel


class Player(BaseModel):
    class Meta:
        table_name = 'players'

    player_id = AutoField(primary_key=True)
    user_id = ForeignKeyField(user.User.user_id, backref="players")
    skin_id = ForeignKeyField(skin.Skin.skin_id, backref="players")
    uuid = UUIDField(default='', unique=True, null=False)
    player_name = CharField(unique=True)

