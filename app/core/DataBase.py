from peewee import SqliteDatabase
from aioredis import Redis
import aioredis

from config.app import settings as AppConfig

from config.redis import settings as RedisConfig

db = SqliteDatabase(AppConfig.BASE_PATH + '\\test.db')


async def sys_cache() -> Redis:
    """
        系统缓存
        :return: cache 连接池
    """
    pool = aioredis.ConnectionPool(
        host=RedisConfig.HOST,
        port=RedisConfig.PORT,
        db=0,
        decode_responses=True
    )
    return Redis(
        connection_pool=pool
    )


async def code_cache() -> Redis:
    """
        系统缓存
        :return: cache 连接池
    """
    pool = aioredis.ConnectionPool(
        host=RedisConfig.HOST,
        port=RedisConfig.PORT,
        db=1,
        decode_responses=True
    )
    return Redis(
        connection_pool=pool
    )
