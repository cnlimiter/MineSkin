from peewee import AutoField, CharField, ForeignKeyField, IntegerField

from app.models import user
from app.models.base_model import BaseModel


class Token(BaseModel):
    class Meta:
        table_name = 'tokens'

    token_id = AutoField(primary_key=True)
    user_id = ForeignKeyField(user.User.user_id, backref="users")
    access_token = CharField(default='', null=False)
    client_token = CharField(default='', null=False)
    status = IntegerField(default=1)

    def can_use(self):
        return self.status != 0
