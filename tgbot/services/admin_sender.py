from aiogram import types, Bot

from tgbot import texts
from tgbot.config import Config
from tgbot.constants._types import MenuPart
from tgbot.keyboards.inline import confirm_inline_keyboard


async def send_reg_info_to_admin(bot: Bot, config: Config, fill_template_text: str, photo_ids: list, video_ids: list,
                                 verification_photo_id: str, from_user_id: int, change_account_data: bool):
    first_media_part = types.InputMediaPhoto(media=photo_ids[0], caption=fill_template_text)
    media = [first_media_part] + [
        types.InputMediaPhoto(media=photo_id) for photo_id in photo_ids[1:]
    ]
    media.extend([types.InputMediaVideo(media=video_id) for video_id in video_ids])

    media.append(types.InputMediaPhoto(media=verification_photo_id))

    messages = await bot.send_media_group(
        chat_id=config.tg_bot.admin_ids[0],
        media=media
    )
    last_message = messages[-1]

    if change_account_data:
        text = texts.confirm_change_account_data_text.format(tg_user_id=from_user_id)
        payload = f'{from_user_id}_c'
    else:
        text = texts.confirm_user_reg_data_text.format(tg_user_id=from_user_id)
        payload = str(from_user_id)

    await bot.send_message(
        chat_id=config.tg_bot.admin_ids[0],
        reply_to_message_id=last_message.message_id,
        text=text,
        reply_markup=confirm_inline_keyboard(payload=payload, reject=True, extra=MenuPart.review_reg_data)
    )
