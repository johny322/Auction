import asyncio

from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import Column, BigInteger

from tgbot.config import load_config

config = load_config('.env')
db_config = config.db
db = Gino()


# Документация
# http://gino.fantix.pro/en/latest/tutorials/tutorial.html

async def create_db():
    POSTGRES_URI = f"postgresql://{db_config.user}:{db_config.password}@{db_config.host}/{db_config.database}"
    # Устанавливаем связь с базой данных
    await db.set_bind(POSTGRES_URI)
    db.gino: GinoSchemaVisitor

    # Создаем таблицы
    # await db.gino.drop_all()
    await db.gino.create_all()


async def add_column(table_name, column):
    POSTGRES_URI = f"postgresql://{db_config.user}:{db_config.password}@{db_config.host}/{db_config.database}"
    # Устанавливаем связь с базой данных
    engine = await db.set_bind(POSTGRES_URI)
    async with engine.acquire() as conn:
        column_name = column.compile(dialect=conn.dialect)
        column_type = column.type.compile(conn.dialect)

        res = 'ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type)
        print(res)

        result = await conn.status(res)
        print(result)


if __name__ == '__main__':
    table_name = 'users'

    column = Column('referral', BigInteger)
    asyncio.run(add_column(table_name, column))
