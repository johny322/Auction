from typing import Union

from sqlalchemy import (
    URL
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine as _create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from tgbot.config import load_config

config = load_config('.env')
db_config = config.db


def create_async_engine(url: Union[URL, str]) -> AsyncEngine:
    engine: AsyncEngine = _create_async_engine(
        url=url,
        # echo=True,
    )
    return engine


def create_session_maker(engine: AsyncEngine = None) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        engine or create_async_engine(db_config.create_url()),
        expire_on_commit=False
    )
