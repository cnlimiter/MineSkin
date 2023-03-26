from contextvars import ContextVar

from peewee import _ConnectionState, SqliteDatabase

from config.config import settings as app_config

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(_ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


async def reset_db_state():
    db._state._state.set(db_state_default.copy())
    db._state.reset()


db = SqliteDatabase(app_config.BASE_PATH + '\\test.db')

# db = MySQLDatabase(
#     settings.DATABASE,
#     user=settings.USER,
#     host=settings.HOST,
#     password=settings.PASSWORD,
#     port=settings.PORT
# )

# db._state = PeeweeConnectionState()
