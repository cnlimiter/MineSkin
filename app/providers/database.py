from peewee import SqliteDatabase

from config.app import settings as app_config

db = SqliteDatabase(app_config.BASE_PATH + '\\test.db')
