from aiogram import Bot

from tgbot.config import Config
from tgbot.keyboards.inline import bet_chanel_inline_keyboard


async def edit_auction_message(bot: Bot, auction_message_id: int, text: str, bet_size: int, config: Config):
    tg_bot_config = config.tg_bot
    await bot.edit_message_text(
        text=text,
        chat_id=tg_bot_config.main_chanel_id,
        message_id=auction_message_id,
        reply_markup=bet_chanel_inline_keyboard(bet_size, tg_bot_config.bot_link())
    )
