from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.db import db_commands
from tgbot.filters.admin import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(Command('cities'))
async def cities_handler(message: types.Message, session: AsyncSession):
    print(await db_commands.get_girls_cities(session))
    girls_data = await db_commands.get_users_data(session)
    for girl_data in girls_data:
        print(girl_data.get_reg_kwargs())
