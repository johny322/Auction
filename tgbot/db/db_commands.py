import asyncio
from typing import List

from sqlalchemy import and_, desc

from tgbot.db.database import db
from tgbot.db.models import User, Favorite, Settings


async def add_user(**kwargs):
    new_user = await User(**kwargs).create()
    await Settings(user_id=new_user.id).create()
    return new_user


async def update_user(user_id, **kwargs):
    # user = await User.query.where(User.user_id == user_id).gino.first()
    # if user:
    #     await user.update(**kwargs).apply()
    return await User.update.values(**kwargs).where(User.user_id == user_id).gino.status()


async def get_user(user_id) -> User:
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def get_users_count() -> int:
    count = await db.func.count(User.id).gino.scalar()
    return count


async def get_user_referrals_count(user_id) -> int:
    count = await db.select([db.func.count()]).where(
        User.referral == user_id
    ).gino.scalar()
    return count


async def add_user_favorite(user_id, service_code, country_code, operator):
    favorites = await Favorite(
        user_id=user_id,
        service_code=service_code,
        country_code=country_code,
        operator_code=operator
    ).create()
    return favorites


async def get_user_favorite(user_id, service_code, country_code, operator_code):
    return await Favorite.query.where(
        and_(
            Favorite.user_id == user_id,
            Favorite.service_code == service_code,
            Favorite.country_code == country_code,
            Favorite.operator_code == operator_code
        )
    ).gino.first()


async def get_users_with_balance(min_balance=0):
    users = await User.query.where(
        User.balance > min_balance
    ).order_by(desc(User.balance)).gino.all()
    return users


async def get_user_favorite_count(user_id):
    count = await db.select([db.func.count()]).where(
        Favorite.user_id == user_id
    ).gino.scalar()
    return count


if __name__ == '__main__':
    asyncio.run(update_user(12312312, balance=22))
