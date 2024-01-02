import asyncio
from typing import Optional, Union, Sequence, Tuple, List

from sqlalchemy import select, delete, update, func, exists, FetchedValue
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tgbot.config import load_config
from tgbot.constants import consts
from tgbot.constants.consts import ADMIN_PERCENT, MINIMAL_BET_SIZE
from tgbot.misc.utils.date_worker import get_now_datetime
from .database import create_session_maker, create_async_engine
from .models import User, BaseModel, BotSettings, Auction, AuctionHistory, AuctionStatus, Payout

"""
во всех функциях объект session: AsyncSession передается после выполнения кода ниже, 
т.е. в самой функции не надо делать закрытие сессии и commit, это сделается автоматически

    async with async_session() as session:  # type: AsyncSession
        async with session.begin():

объект session будет пробрасываться в хендлеры через мидлварь
"""

MODEL = Union[User, BaseModel, BotSettings, Auction, AuctionHistory]


# MODEL = Union[Type[User], Type[UserPhoto], Type[UserData], Type[CityModel], Type[View], Type[SubscriptionTypeModel]]

async def create_db() -> None:
    config = load_config('.env')
    db_config = config.db
    engine = create_async_engine(db_config.create_url())
    async with engine.begin() as conn:  # type: AsyncConnection
        await conn.run_sync(BaseModel.metadata.create_all)


async def add_object(session: AsyncSession, model: MODEL, **kwargs) -> Optional[MODEL]:
    new_obj = model(**kwargs)
    session.add(new_obj)
    if new_obj:
        return new_obj
    return None


async def get_object(session: AsyncSession, model: MODEL, model_id: int) -> Optional[MODEL]:
    res = await session.get(model, model_id)
    return res


async def add_user(session: AsyncSession, **kwargs) -> Optional[User]:
    new_user = User(**kwargs)
    session.add(new_user)
    if new_user:
        return new_user
    return None


async def users_to_mails(session: AsyncSession) -> Sequence[User]:
    stmt = select(User).where(User.disable_ads == False)
    res = await session.scalars(stmt)
    return res.all()


# async def get_user_photos(session: AsyncSession, user_id: int) -> Sequence[UserPhoto]:
#     """unblur photos"""
#         stmt = select(UserPhoto).where(UserPhoto.user.has(id=user_id), UserPhoto.blur == False)
#         res = await session.scalars(stmt)
#         user_photos = res.all()
#         return user_photos
#
#
# async def get_all_user_photos(session: AsyncSession, user_id: int) -> Sequence[UserPhoto]:
#     stmt = select(UserPhoto).where(UserPhoto.user.has(id=user_id))
#     res = await session.scalars(stmt)
#     user_photos = res.all()
#     return user_photos
#
#
# async def add_user_photos(session: AsyncSession, **kwargs) -> Optional[UserPhoto]:
#     new_obj = await add_object(session, UserPhoto, **kwargs)
#     return new_obj
#
#
# async def get_user_blur_photos(session: AsyncSession, user_id: int) -> Sequence[UserPhoto]:
#     stmt = select(UserPhoto).where(UserPhoto.user.has(id=user_id), UserPhoto.blur == True)
#     res = await session.scalars(stmt)
#     user_photos = res.all()
#     return user_photos
#
#
# async def add_user_verification_photo(session: AsyncSession, **kwargs) -> UserVerificationPhoto:
#     new_obj = await add_object(session, UserVerificationPhoto, **kwargs)
#     return new_obj
#
#
# async def get_last_user_verification_photo(session: AsyncSession, user_id: int = None, tg_user_id: int = None) -> \
#         Optional[UserVerificationPhoto]:
#     if user_id is not None:
#         filter_ = UserVerificationPhoto.user_id == user_id
#     else:
#         filter_ = User.tg_user_id == tg_user_id
#     stmt = select(UserVerificationPhoto).join(User).where(**filter_).order_by(
#         UserVerificationPhoto.updated_at
#     )
#     res = await session.scalar(stmt)
#     return res
#
#
# async def add_user_data(session: AsyncSession, **kwargs) -> UserData:
#     new_obj = await add_object(session, UserData, **kwargs)
#     return new_obj
#
#
# async def get_users_data_by_city(session: AsyncSession, user_type: UserType, city_full_name: str) -> Sequence[UserData]:
#     # stmt = select(UserData).where(UserData.user_type == user_type, UserData.city == city)
#     # stmt = select(UserData).where(UserData.user_type.has(name=user_type), UserData.city.has(full_name=city))
#     stmt = select(UserData).join(UserType).join(CityModel).where(
#         UserType.name == user_type, CityModel.full_name == city_full_name
#     )
#     res = await session.scalars(stmt)
#     return res.all()
#
#
# async def get_cities_by_user_type(session: AsyncSession, user_type: str) -> Sequence[str]:
#     stmt = select(CityModel.full_name).select_from(User).join(UserData.city) \
#         .where(UserData.user_type.has(name=user_type)).distinct()
#     res = await session.scalars(stmt)
#     return res.all()
#
#
# async def get_cities_data_by_user_type(session: AsyncSession, user_type: str) -> Sequence[CityModel]:
#     stmt = select(CityModel).select_from(User).join(UserData.city) \
#         .where(UserData.user_type.has(name=user_type)).distinct()
#     res = await session.scalars(stmt)
#     return res.all()
#
#
# async def get_girls_cities(session: AsyncSession) -> Sequence[str]:
#     stmt = select(CityModel.full_name).join(UserData.city) \
#         .where(UserData.user_type.has(name='girl')).distinct()
#     res = await session.scalars(stmt)
#     return res.all()
#
#
# async def get_user_data(session: AsyncSession, user_id) -> Optional[UserData]:
#     stmt = select(UserData).where(UserData.user_id == user_id)
#     res = await session.scalar(stmt)
#     return res
#
#
# async def get_users_data(session: AsyncSession) -> Sequence[UserData]:
#     return (await session.scalars(select(UserData))).all()
#
#
# async def update_user_data(session: AsyncSession, user_id: int, **kwargs) -> Sequence[UserData]:
#     stmt = update(UserData).where(UserData.user_id == user_id).values(**kwargs).returning(UserData)
#     res = await session.execute(stmt)
#     await session.flush()
#     return res.scalars().all()
#
#
# async def delete_user_data(session: AsyncSession, user_id: int) -> None:
#     stmt = delete(UserData).where(UserData.user_id == user_id)
#     res = await session.execute(stmt)
#     stmt = delete(UserPhoto).where(UserPhoto.user_id == user_id)
#     res = await session.execute(stmt)
#     await session.flush()
#
#
# async def full_delete_user(session: AsyncSession, tg_user_id: int, user: User = None) -> None:
#     if user is None:
#         user = await get_user(session, tg_user_id)
#     if not user:
#         return
#     stmt1 = delete(User).where(User.tg_user_id == tg_user_id)
#     stmt2 = delete(UserData).where(UserData.user == user)
#     stmt3 = delete(UserPhoto).where(UserPhoto.user == user)
#
#     await session.execute(stmt1)
#     await session.execute(stmt2)
#     await session.execute(stmt3)
#     await session.flush()


async def update_user(session: AsyncSession, tg_user_id, **kwargs) -> Optional[User]:
    stmt = update(User).where(User.tg_user_id == tg_user_id).values(**kwargs).returning(User)
    res = await session.scalar(stmt)
    await session.flush()
    return res


async def update_user_by_db_id(session: AsyncSession, user_id, **kwargs):
    stmt = update(User).where(User.id == user_id).values(**kwargs).returning(User)
    res = await session.scalar(stmt)
    await session.flush()
    return res


async def get_user(session: AsyncSession, tg_user_id: int) -> Optional[User]:
    stmt = select(User).where(User.tg_user_id == tg_user_id)
    res = await session.scalar(stmt)
    return res


async def get_user_by_db_id(session: AsyncSession, user_id: int) -> Optional[User]:
    stmt = select(User).where(User.id == user_id)
    res = await session.scalar(stmt)
    return res


async def get_users_count(session: AsyncSession) -> int:
    stmt = select(func.count(User.id))
    res = await session.scalar(stmt)
    return res


async def get_users_with_balance(session: AsyncSession, min_balance=0) -> Sequence[User]:
    stmt = select(User).where(User.balance > min_balance)
    res = await session.scalars(stmt)
    return res.all()


async def get_bot_settings(session: AsyncSession) -> Optional[BotSettings]:
    stmt = select(BotSettings)
    res = await session.scalar(stmt)
    return res


async def update_bot_settings(session: AsyncSession, bot_settings_id: int, **kwargs) -> BotSettings:
    stmt = update(BotSettings).where(BotSettings.id == bot_settings_id).values(**kwargs).returning(BotSettings)
    res = await session.scalar(stmt)
    await session.flush()
    return res


async def add_start_settings(async_session: async_sessionmaker[AsyncSession]):
    async with async_session() as session:  # type: AsyncSession
        async with session.begin():
            bot_settings = await get_bot_settings(session)
            if bot_settings:
                return bot_settings
            await add_object(
                session, BotSettings,
                admin_percent=ADMIN_PERCENT,
                minimal_bet_size=MINIMAL_BET_SIZE
            )


async def get_auction(session: AsyncSession, auction_id: int) -> Optional[Auction]:
    return await get_object(session, Auction, auction_id)


async def add_auction(session: AsyncSession, **kwargs) -> Tuple[Auction, AuctionHistory]:
    auction = await add_object(
        session, Auction,
        **kwargs
    )
    await session.flush()
    auction_history = await add_object(
        session, AuctionHistory,
        auction_id=auction.id,
        bet=kwargs['last_bet_sum'],
        user_id=kwargs['creator_id']
    )
    await session.flush()
    return auction, auction_history


async def update_auction(session: AsyncSession, auction_id: int, **kwargs) -> Tuple[Auction, AuctionHistory]:
    stmt = update(Auction).where(Auction.id == auction_id).values(**kwargs).returning(Auction)
    auction = await session.scalar(stmt)
    await session.flush()
    auction_history = await add_object(
        session, AuctionHistory,
        auction_id=auction.id,
        bet=kwargs.get('last_bet_sum') or auction.last_bet_sum,
        user_id=kwargs.get('last_user_id') or auction.last_user_id
    )
    await session.flush()
    return auction, auction_history


async def has_active_auction(session: AsyncSession) -> Optional[Auction]:
    stmt = select(Auction).where(Auction.status == AuctionStatus.active.value)
    res = await session.scalar(stmt)
    return res


async def get_payout(session: AsyncSession, payout_id) -> Optional[Payout]:
    payout = await get_object(
        session, Payout, payout_id
    )
    await session.flush()
    return payout


async def add_payout(session: AsyncSession, **kwargs) -> Payout:
    payout = await add_object(
        session, Payout,
        **kwargs
    )
    await session.flush()
    return payout


async def update_payout(session: AsyncSession, payout_id: int, **kwargs) -> Payout:
    stmt = update(Payout).where(Payout.id == payout_id).values(**kwargs).returning(Payout)
    payout = await session.scalar(stmt)
    await session.flush()
    return payout


async def return_auction_balance(session: AsyncSession, auction_id: int) -> dict:
    auction = await get_auction(session, auction_id)
    history: List[AuctionHistory] = await auction.awaitable_attrs.history
    users_bets_data = {}
    for h in history:
        user_id = h.user_id
        if user_id not in users_bets_data:
            users_bets_data[user_id] = 0
        users_bets_data[user_id] += h.bet
    for user_id, bets_size in users_bets_data.items():
        stmt = update(User).where(User.id == user_id).values(balance=User.balance + bets_size)
        await session.execute(stmt)
        await session.flush()
    return users_bets_data


# async def add_auction_history(session: AsyncSession, **kwargs) -> Optional[Auction]:
#     return await add_object(
#         session, Auction,
#         **kwargs
#     )


async def test():
    config = load_config('.env')
    db_config = config.db
    engine = create_async_engine(db_config.create_url())
    async_session = create_session_maker()
    async with engine.begin() as conn:  # type: AsyncConnection
        await conn.run_sync(BaseModel.metadata.create_all)
    async with async_session() as session:  # type: AsyncSession
        async with session.begin():
            pass


if __name__ == '__main__':
    asyncio.run(test())
