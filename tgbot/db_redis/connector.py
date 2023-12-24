import asyncio
from typing import Union

import redis.asyncio as redis

from tgbot.config import load_config


class RedisConnector:
    __redis_connection: redis.Redis = None

    def __init__(self):
        self._connection = self.get_connection()

    @classmethod
    def get_connection(cls) -> redis.Redis:
        if cls.__redis_connection is None:
            print('get redis conn')
            config = load_config('.env')
            kwargs = config.db_redis.get_kwargs()

            pool = redis.ConnectionPool(**kwargs)
            redis_connection = redis.Redis(connection_pool=pool)
            cls.__redis_connection = redis_connection
        return cls.__redis_connection

    @classmethod
    async def close(cls) -> None:
        if cls.__redis_connection is not None:
            print('close')
            await cls.__redis_connection.close()
            await cls.__redis_connection.connection_pool.disconnect()

    async def set_list_values(self, key: str, *values: Union[str, int, bytes, float]) -> str:
        return await self._connection.lpush(key, *values)

    async def get_list_values(self, key: str, val_type=int) -> list:
        names = [val_type(name) for name in await self._connection.lrange(key, 0, -1)]
        return names

    async def get_value(self, key: str) -> bytes:
        return await self._connection.get(key)

    async def set_value(self, key: str, value: str) -> str:
        return await self._connection.set(key, value)

    async def del_value(self, key: str) -> str:
        return await self._connection.delete(key)


async def test():
    rc = RedisConnector()
    r = await rc.set_list_values('ttt', *[1, 2, 222, 1, '1'])
    print(r)
    print(await rc.get_list_values('ttt'))
    await rc.del_value('ttt')

    rc = RedisConnector()
    r = await rc.set_list_values('ttt', *[1, 2, 222, 1, '1'])
    print(r)
    print(await rc.get_list_values('ttt'))
    await rc.del_value('ttt')


if __name__ == '__main__':
    asyncio.run(test())
