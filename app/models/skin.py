from peewee import AutoField, CharField, IntegerField, ForeignKeyField, BooleanField

from app.models.user import User
from app.models.base import BaseModel


class Skin(BaseModel):
    class Meta:
        table_name = 'skins'

    skin_id = AutoField(primary_key=True)
    name = CharField(default='')
    type = CharField(default='steve', null=False)
    hash = CharField(default='9b155b4668427669ca9ed3828024531bc52fca1dcf8fbde8ccac3d9d9b53e3cf')
    likes = IntegerField(default=0)
    uploader = ForeignKeyField(User.user_id, backref='users')
    public = BooleanField(default=True)

    def is_alex(self):
        return self.type == 'alex'

    def is_steve(self):
        return self.type == 'steve'

    def is_cape(self):
        return self.type == 'cape'
