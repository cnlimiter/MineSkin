from peewee import ForeignKeyField

from app.models.base import BaseModel
from app.models.skin import Skin
from app.models.user import User


class Closet(BaseModel):
    class Meta:
        table_name = 'closets'

    user_id = ForeignKeyField(User.user_id, backref="users", unique=True)
    skin_id = ForeignKeyField(Skin.skin_id, backref="skins")
