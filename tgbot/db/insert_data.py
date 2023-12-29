import asyncio
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.config import load_config
from tgbot.db import db_commands
from .database import create_async_engine, create_session_maker
from .models import BaseModel, User

config = load_config('.env')
db_config = config.db
engine = create_async_engine(db_config.create_url())
async_session = create_session_maker()


async def insert_start_data():
    async with engine.begin() as conn:  # type: AsyncConnection
        await conn.run_sync(BaseModel.metadata.create_all)
    async with async_session() as session:  # type: AsyncSession
        async with session.begin():
            admin_ids = config.tg_bot.admin_ids
            stmt = update(User).where(User.tg_user_id.in_(admin_ids), is_admin=False)
            res = await session.execute(stmt)
            # await session.flush()
            print(res.scalars().all())


async def insert_start_test_data():
    async with engine.begin() as conn:  # type: AsyncConnection
        await conn.run_sync(BaseModel.metadata.create_all)

    async with async_session() as session:  # type: AsyncSession
        async with session.begin():
            pass


if __name__ == '__main__':
    asyncio.run(insert_start_test_data())
