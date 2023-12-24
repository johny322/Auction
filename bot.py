import asyncio
import logging
from typing import List

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.config import load_config
from tgbot.constants.consts import MAIN_LOGO_FILE_PATH, MAIN_LOGO_FILE
from tgbot.db.database import create_session_maker
from tgbot.db.db_commands import add_start_settings
from tgbot.db_redis.connector import RedisConnector
from tgbot.handlers.admin import admin_router
from tgbot.handlers.echo import echo_router
from tgbot.handlers.users import user_router
from tgbot.middlewares.actions import ChatActionMiddleware
from tgbot.middlewares.agreement import AgreementMiddleware
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.middlewares.db_objects import GetDbObjectsMiddleware
from tgbot.middlewares.db_session import DbSessionMiddleware
from tgbot.middlewares.objects import GetObjectsMiddleware
from tgbot.middlewares.throttling import ThrottlingMiddleware
from tgbot.misc.bot_commands import set_bot_commands
from tgbot.services import broadcaster
from tgbot.services.telegraph import TelegraphService

config = load_config(".env")


def setup_logger():
    logger = logging.getLogger('main_logger')
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    strfmt = "[%(asctime)s] [%(levelname)-8s] --- %(message)s (%(filename)s:%(funcName)s:%(lineno)s)"

    datefmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(strfmt, datefmt)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.info('Set up logger')

    return logger


logger = setup_logger()


async def on_startup(bot: Bot, admin_ids: List[int], async_session: AsyncSession):
    # делаем alembic
    # await create_db()
    logger.debug('db created')
    await add_start_settings(async_session)
    await set_bot_commands(bot, admin_ids)
    await broadcaster.broadcast(bot, admin_ids, "Бот был запущен")


async def on_shutdown(bot: Bot, ts: TelegraphService):
    await ts.close()


def register_global_middlewares(dp: Dispatcher, config, bot, logger, async_session, **kwargs):
    dp.message.outer_middleware(DbSessionMiddleware(async_session))
    dp.callback_query.outer_middleware(DbSessionMiddleware(async_session))
    dp.inline_query.outer_middleware(DbSessionMiddleware(async_session))

    # dp.message.outer_middleware(AntiFloodMiddleware(redis_storage))
    # dp.callback_query.outer_middleware(AntiFloodMiddleware(redis_storage))
    # dp.inline_query.outer_middleware(AntiFloodMiddleware(redis_storage))

    dp.message.outer_middleware(ThrottlingMiddleware())
    dp.callback_query.outer_middleware(ThrottlingMiddleware())
    dp.inline_query.outer_middleware(ThrottlingMiddleware())

    dp.message.outer_middleware(AgreementMiddleware(async_session))
    dp.callback_query.outer_middleware(AgreementMiddleware(async_session))
    dp.inline_query.outer_middleware(AgreementMiddleware(async_session))

    dp.message.middleware(ChatActionMiddleware())
    dp.callback_query.middleware(ChatActionMiddleware())

    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))

    dp.message.middleware(GetObjectsMiddleware(logger=logger, bot=bot, **kwargs))
    dp.callback_query.middleware(GetObjectsMiddleware(logger=logger, bot=bot, **kwargs))
    dp.message.middleware(GetDbObjectsMiddleware())
    dp.callback_query.middleware(GetDbObjectsMiddleware())
    dp.inline_query.middleware(GetDbObjectsMiddleware())


async def main():
    logger.info("Starting bot")

    storage = MemoryStorage()

    # storage.redis.set()
    redis_connector = RedisConnector()
    # redis_storage = RedisStorage(redis_connector.get_connection())

    dp = Dispatcher(storage=storage)
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    for router in [
        admin_router,
        user_router,
        echo_router,
    ]:
        dp.include_router(router)

    ts = TelegraphService()

    main_logo_file = types.FSInputFile(
        path=MAIN_LOGO_FILE_PATH,
        filename=MAIN_LOGO_FILE,
    )
    async_session = create_session_maker()

    register_global_middlewares(
        dp, config, logger=logger, bot=bot, ts=ts, redis_connector=redis_connector, main_logo_file=main_logo_file,
        async_session=async_session
    )

    await on_startup(bot, config.tg_bot.admin_ids, async_session)
    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()
        await on_shutdown(bot, ts)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот был выключен!")
