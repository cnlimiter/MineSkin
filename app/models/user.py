from peewee import CharField, IntegerField, AutoField, UUIDField, ForeignKeyField

from app.models.base_model import BaseModel


class User(BaseModel):
    class Meta:
        table_name = 'users'

    user_id = AutoField(primary_key=True)
    username = CharField(unique=True)
    uuid = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    score = IntegerField(default=0)
    avatar = CharField(null=True)
    permission = IntegerField(default=0)

    def is_enabled(self):
        return self.permission != -1

    def is_admin(self):
        return self.permission == 99

    def is_super_admin(self):
        return self.permission == 100
