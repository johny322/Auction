from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat


async def set_bot_commands(bot: Bot, admin_ids):
    await bot.set_my_commands(
        commands=[
            BotCommand(
                command='start',
                description='🤖 Перезапустить бота'
            )
        ]
    )
    for admin in admin_ids:
        await bot.set_my_commands(
            commands=[
                BotCommand(
                    command='start',
                    description='🤖 Перезапустить бота'
                ),
                BotCommand(
                    command='admin',
                    description='Список команд админа'
                )
            ],
            scope=BotCommandScopeChat(
                chat_id=admin
            )
        )
