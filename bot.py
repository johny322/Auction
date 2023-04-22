import asyncio
import logging
from typing import List

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage

from tgbot.config import load_config
from tgbot.db.database import create_db
from tgbot.handlers.admin import admin_router
from tgbot.handlers.users import user_router
from tgbot.middlewares.actions import ChatActionMiddleware
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.middlewares.objects import GetObjectsMiddleware
from tgbot.middlewares.users import GetUserMiddleware
from tgbot.misc.bot_commands import set_bot_commands
from tgbot.services import broadcaster

config = load_config(".env")


def setup_logger():
    logger = logging.getLogger('main_logger')
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    # strfmt = '[%(asctime)s] [%(levelname)s] %(message)s'
    strfmt = "[%(asctime)s] [%(levelname)-8s] --- %(message)s (%(filename)s:%(funcName)s:%(lineno)s)"

    datefmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(strfmt, datefmt)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.info('Set up logger')
    # logger.info('Set up logger', extra={'d': {'detail': 'new line'}})

    return logger


logger = setup_logger()


async def on_startup(bot: Bot, admin_ids: List[int]):
    await create_db()
    await set_bot_commands(bot, admin_ids)
    await broadcaster.broadcast(bot, admin_ids, "Бот был запущен")


def register_global_middlewares(dp: Dispatcher, config, bot, logger):
    dp.message.middleware(ChatActionMiddleware())
    dp.callback_query.middleware(ChatActionMiddleware())

    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))

    dp.message.middleware(GetObjectsMiddleware(logger=logger, bot=bot))
    dp.callback_query.middleware(GetObjectsMiddleware(logger=logger, bot=bot))
    dp.message.middleware(GetUserMiddleware())
    dp.callback_query.middleware(GetUserMiddleware())


async def main():
    logger.info("Starting bot")

    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    for router in [
        admin_router,
        user_router,
        # echo_router,
    ]:
        dp.include_router(router)

    register_global_middlewares(
        dp, config, logger=logger, bot=bot
    )

    await on_startup(bot, config.tg_bot.admin_ids)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот был выключен!")
