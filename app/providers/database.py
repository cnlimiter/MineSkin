from peewee import SqliteDatabase
import redis

from config.app import settings as AppConfig

from config.redis import settings as RedisConfig

db = SqliteDatabase(AppConfig.BASE_PATH + '\\test.db')

pool = redis.ConnectionPool(
    host=RedisConfig.HOST,
    port=RedisConfig.PORT,
    db=RedisConfig.DB,
    decode_responses=True
)

redis = redis.Redis(
    connection_pool=pool
)
