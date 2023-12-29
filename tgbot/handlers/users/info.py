from aiogram import Router, F, types
from aiogram.utils import keyboard

from tgbot import texts
from tgbot.config import Config
from tgbot.keyboards import reply
from tgbot.texts import keyboard_texts

info_router = Router()


@info_router.message(F.text == keyboard_texts.btn_menu_info)
async def info_handler(message: types.Message):
    await message.answer(
        text=texts.choose_menu_text,
        reply_markup=reply.info_menu()
    )


@info_router.message(F.text == keyboard_texts.btn_to_start_menu)
async def info_handler(message: types.Message):
    await message.answer(
        text=texts.choose_menu_text,
        reply_markup=reply.main_keyboard()
    )


@info_router.message(F.text == keyboard_texts.btn_info_menu_admin)
async def info_handler(message: types.Message, config: Config):
    await message.answer(
        text=texts.admin_info_message_text.format(admin=config.tg_bot.admin_username),
    )


@info_router.message(F.text == keyboard_texts.btn_add_info_auction_chanel)
async def info_handler(message: types.Message):
    await message.answer(
        text=texts.add_auction_message_text,
    )


@info_router.message(F.text == keyboard_texts.btn_info_reserve_chanel)
async def info_handler(message: types.Message, config: Config):
    await message.answer(
        text=texts.info_reserve_chanel_message_text.format(reserve_chanel_url=config.tg_bot.reserve_chanel_url),
    )


@info_router.message(F.text == keyboard_texts.btn_info_auction_chanel)
async def info_handler(message: types.Message, config: Config):
    await message.answer(
        text=texts.info_main_chanel_message_text.format(main_chanel_url=config.tg_bot.main_chanel_url),
    )


@info_router.message(F.text == keyboard_texts.btn_info_payout)
async def info_handler(message: types.Message, config: Config):
    await message.answer(
        text=texts.info_payout_chanel_message_text.format(payout_chanel_url=config.tg_bot.payout_chanel_url),
    )


@info_router.message(F.text == keyboard_texts.btn_info_news_chanel)
async def info_handler(message: types.Message, config: Config):
    await message.answer(
        text=texts.info_news_chanel_message_text.format(news_chanel_url=config.tg_bot.news_chanel_url),
    )


@info_router.message(F.text == keyboard_texts.btn_menu_rules)
async def info_handler(message: types.Message):
    await message.answer(
        text=texts.choose_menu_text,
        reply_markup=reply.rules_menu()
    )


@info_router.message(F.text == keyboard_texts.btn_rules_auction)
async def info_handler(message: types.Message):
    await message.answer(
        text=texts.auction_rules_text,
    )


@info_router.message(F.text == keyboard_texts.btn_rules_bot)
async def info_handler(message: types.Message):
    await message.answer(
        text=texts.bot_rules_text,
    )


@info_router.message(F.text == keyboard_texts.btn_recommend)
async def info_handler(message: types.Message):
    await message.answer(
        text=texts.recommend_message_text,
    )
