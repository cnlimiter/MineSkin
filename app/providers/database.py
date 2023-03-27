from peewee import SqliteDatabase

from config.config import settings as app_config

db = SqliteDatabase(app_config.BASE_PATH + '\\test.db')
