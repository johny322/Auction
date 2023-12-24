# from tgbot.db import db_commands
#
#
# async def insert_sub_type():
#     sub_types_data = [
#         dict(
#             name='7 дней',
#             period_in_days=7,
#             price=299,
#             currency='RUB'
#         ),
#         dict(
#             name='30 дней',
#             period_in_days=30,
#             price=699,
#             currency='RUB'
#         ),
#         dict(
#             name='60 дней',
#             period_in_days=60,
#             price=1599,
#             currency='RUB'
#         ),
#
#     ]
#     sub_types = await db_commands.get_sub_types()
#     if not sub_types:
#         for sub_type_data in sub_types_data:
#             await db_commands.add_sub_types(**sub_type_data)
#
#
# async def insert_start_data():
#     await insert_sub_type()

import asyncio
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.config import load_config
from tgbot.db import db_commands
from .database import create_async_engine, create_session_maker
from .models import BaseModel, SubscriptionTypeModel, UserType, UserStatus, User, CityModel, UserData, View

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
            # file_ids = [
            #     'AgACAgIAAxkBAAKimWUxhxmEI1oPFlPoylPM91oBqDO8AAKJ1jEbwHmRScrAcBiDx4_ZAQADAgADbQADMAQ',
            #     'AgACAgIAAxkBAAKim2Uxhxm94xnQIKo3_p3w_7WDe6ymAAKK1jEbwHmRSUkdgdJ0w9xYAQADAgADeQADMAQ',
            # ]
            # for file_id in file_ids:
            #     await db_commands.add_user_photos(
            #         session,
            #         user_id=2,
            #         file_id=file_id,
            #         file_type='photo',
            #         blur=False,
            #     )
            #     await db_commands.add_user_photos(
            #         session,
            #         user_id=3,
            #         file_id=file_id,
            #         file_type='photo',
            #         blur=False,
            #     )
            pass
            video_id = 'BAACAgIAAxkBAAKimmUxhxkC2okKLp6KA-z7yd8F-lPpAAIPPgACwHmRSSEZ2HPQqROcMAQ'
            await db_commands.add_user_photos(
                session,
                user_id=1,
                file_id=video_id,
                file_type='video',
                blur=False,
            )
            await db_commands.add_user_photos(
                session,
                user_id=2,
                file_id=video_id,
                file_type='video',
                blur=False,
            )
            await db_commands.add_user_photos(
                session,
                user_id=3,
                file_id=video_id,
                file_type='video',
                blur=False,
            )
            file_ids = [
                'https://telegra.ph//file/a39a1357344be133be17c.png',
                'https://telegra.ph//file/b09bbca4af0b5c0d1617c.png',
            ]
            for file_id in file_ids:
                await db_commands.add_user_photos(
                    session,
                    user_id=1,
                    file_id=file_id,
                    file_type='photo',
                    blur=True,
                )
                await db_commands.add_user_photos(
                    session,
                    user_id=2,
                    file_id=file_id,
                    file_type='photo',
                    blur=True,
                )
                await db_commands.add_user_photos(
                    session,
                    user_id=3,
                    file_id=file_id,
                    file_type='photo',
                    blur=True,
                )
            pass
            # ut1 = UserType(name='girl', pretty_name='Девушка')
            # ut2 = UserType(name='boy', pretty_name='Мужчина')
            #
            # us1 = UserStatus(name='common')
            # us2 = UserStatus(name='gold')
            # us3 = UserStatus(name='dimond')
            #
            # stm1 = SubscriptionTypeModel(
            #     name='Месяц', period_in_days=30, price=1000, currency='RUB', user_type_id=2, status_id=2
            # )
            # session.add(stm1)
            #
            # session.add_all(
            #     [
            #         ut1, ut2,
            #         us1, us2, us3,
            #         stm1
            #     ]
            # )
            # user1 = User(
            #     tg_user_id=1233,
            #     username='1233',
            #     full_name='1233',
            #     agreement=True,
            #     status_id=1,
            #     user_type=ut2,
            # )
            # user2 = User(
            #     tg_user_id=2223,
            #     username='2223',
            #     full_name='2223',
            #     agreement=True,
            #     status_id=1,
            #     user_type=ut1,
            # )
            # user3 = User(
            #     tg_user_id=3333,
            #     username='3333',
            #     full_name='3333',
            #     agreement=True,
            #     status_id=1,
            #     user_type=ut1,
            # )
            #
            # session.add_all(
            #     [
            #         user1, user2, user3
            #     ]
            # )
            # cm1 = CityModel(country='Россия', name='Москва', district='Московская обл',
            #                 full_name='Московская обл, Москва')
            # cm2 = CityModel(country='Россия', name='Нижний', district='Московская обл',
            #                 full_name='Московская обл, Нижний')
            # cm3 = CityModel(country='Россия', name='Москва1', district='Московская обл',
            #                 full_name='Московская обл, Москва1')
            # cm4 = CityModel(country='Россия', name='Москва2', district='Московская обл',
            #                 full_name='Московская обл, Москва2')
            #
            # session.add_all(
            #     [cm1, cm2, cm3, cm4, ]
            # )
            # ud1 = UserData(
            #     user_id=2, name='name11', full_name='full_name11', country='Россия',
            #     city_full_name='Московская обл, Москва', birthday=datetime(year=2000, month=1, day=1).date(),
            #     about='about', mobile_phone='mobile_phone', tg='tg', wa=False, breast_size=2.5, height=123,
            #     weight=22, user_type=ut1, city=cm1
            # )
            # ud2 = UserData(
            #     user_id=3, name='name22', full_name='full_name22', country='Россия',
            #     city_full_name='Московская обл, Москва', birthday=datetime(year=2000, month=1, day=1).date(),
            #     about='about2', mobile_phone='mobile_phone', tg='tg', wa=False, breast_size=2.5, height=123,
            #     weight=22, user_type=ut1, city=cm2
            # )
            # session.add_all(
            #     [ud1, ud2]
            # )
            # await session.flush()
            # v1 = View(user_id=2, viewer_user_id=2, profile_view=True)
            # v2 = View(user_id=2, viewer_user_id=1, phone_view=True)
            # v3 = View(user_id=2, viewer_user_id=1, profile_view=True)
            # session.add_all([v1, v2, v3, ])


if __name__ == '__main__':
    asyncio.run(insert_start_test_data())
