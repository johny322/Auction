import asyncio
from typing import Optional, Union, Sequence

from sqlalchemy import select, delete, update, func, exists
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tgbot.config import load_config
from tgbot.constants import consts
from .database import create_session_maker, create_async_engine
from .models import User, UserPhoto, UserData, CityModel, View, SubscriptionTypeModel, BaseModel, UserType, UserStatus, \
    UserVerificationPhoto, BotSettings

"""
во всех функциях объект session: AsyncSession передается после выполнения кода ниже, 
т.е. в самой функции не надо делать закрытие сессии и commit, это сделается автоматически

    async with async_session() as session:  # type: AsyncSession
        async with session.begin():

объект session будет пробрасываться в хендлеры через мидлварь
"""

MODEL = Union[User, UserPhoto, UserData, CityModel, View, SubscriptionTypeModel]


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


async def get_user_photos(session: AsyncSession, user_id: int) -> Sequence[UserPhoto]:
    """unblur photos"""
    stmt = select(UserPhoto).where(UserPhoto.user.has(id=user_id), UserPhoto.blur == False)
    res = await session.scalars(stmt)
    user_photos = res.all()
    return user_photos


async def get_all_user_photos(session: AsyncSession, user_id: int) -> Sequence[UserPhoto]:
    stmt = select(UserPhoto).where(UserPhoto.user.has(id=user_id))
    res = await session.scalars(stmt)
    user_photos = res.all()
    return user_photos


async def add_user_photos(session: AsyncSession, **kwargs) -> Optional[UserPhoto]:
    new_obj = await add_object(session, UserPhoto, **kwargs)
    return new_obj


async def get_user_blur_photos(session: AsyncSession, user_id: int) -> Sequence[UserPhoto]:
    stmt = select(UserPhoto).where(UserPhoto.user.has(id=user_id), UserPhoto.blur == True)
    res = await session.scalars(stmt)
    user_photos = res.all()
    return user_photos


async def add_user_verification_photo(session: AsyncSession, **kwargs) -> UserVerificationPhoto:
    new_obj = await add_object(session, UserVerificationPhoto, **kwargs)
    return new_obj


async def get_last_user_verification_photo(session: AsyncSession, user_id: int = None, tg_user_id: int = None) -> \
        Optional[UserVerificationPhoto]:
    if user_id is not None:
        filter_ = UserVerificationPhoto.user_id == user_id
    else:
        filter_ = User.tg_user_id == tg_user_id
    stmt = select(UserVerificationPhoto).join(User).where(**filter_).order_by(
        UserVerificationPhoto.updated_at
    )
    res = await session.scalar(stmt)
    return res


async def add_user_data(session: AsyncSession, **kwargs) -> UserData:
    new_obj = await add_object(session, UserData, **kwargs)
    return new_obj


async def get_users_data_by_city(session: AsyncSession, user_type: UserType, city_full_name: str) -> Sequence[UserData]:
    # stmt = select(UserData).where(UserData.user_type == user_type, UserData.city == city)
    # stmt = select(UserData).where(UserData.user_type.has(name=user_type), UserData.city.has(full_name=city))
    stmt = select(UserData).join(UserType).join(CityModel).where(
        UserType.name == user_type, CityModel.full_name == city_full_name
    )
    res = await session.scalars(stmt)
    return res.all()


async def get_cities_by_user_type(session: AsyncSession, user_type: str) -> Sequence[str]:
    stmt = select(CityModel.full_name).select_from(User).join(UserData.city) \
        .where(UserData.user_type.has(name=user_type)).distinct()
    res = await session.scalars(stmt)
    return res.all()


async def get_cities_data_by_user_type(session: AsyncSession, user_type: str) -> Sequence[CityModel]:
    stmt = select(CityModel).select_from(User).join(UserData.city) \
        .where(UserData.user_type.has(name=user_type)).distinct()
    res = await session.scalars(stmt)
    return res.all()


async def get_girls_cities(session: AsyncSession) -> Sequence[str]:
    stmt = select(CityModel.full_name).join(UserData.city) \
        .where(UserData.user_type.has(name='girl')).distinct()
    res = await session.scalars(stmt)
    return res.all()


async def get_user_data(session: AsyncSession, user_id) -> Optional[UserData]:
    stmt = select(UserData).where(UserData.user_id == user_id)
    res = await session.scalar(stmt)
    return res


async def get_users_data(session: AsyncSession) -> Sequence[UserData]:
    return (await session.scalars(select(UserData))).all()


async def update_user_data(session: AsyncSession, user_id: int, **kwargs) -> Sequence[UserData]:
    stmt = update(UserData).where(UserData.user_id == user_id).values(**kwargs).returning(UserData)
    res = await session.execute(stmt)
    await session.flush()
    return res.scalars().all()


async def delete_user_data(session: AsyncSession, user_id: int) -> None:
    stmt = delete(UserData).where(UserData.user_id == user_id)
    res = await session.execute(stmt)
    stmt = delete(UserPhoto).where(UserPhoto.user_id == user_id)
    res = await session.execute(stmt)
    await session.flush()


async def full_delete_user(session: AsyncSession, tg_user_id: int, user: User = None) -> None:
    if user is None:
        user = await get_user(session, tg_user_id)
    if not user:
        return
    stmt1 = delete(User).where(User.tg_user_id == tg_user_id)
    stmt2 = delete(UserData).where(UserData.user == user)
    stmt3 = delete(UserPhoto).where(UserPhoto.user == user)

    await session.execute(stmt1)
    await session.execute(stmt2)
    await session.execute(stmt3)
    await session.flush()


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


async def get_user_referrals_count(session: AsyncSession, user_id: int) -> int:
    stmt = select(func.count(User.id)).where(User.referral_user_id == user_id)
    res = await session.scalar(stmt)
    return res


async def get_users_with_balance(session: AsyncSession, min_balance=0) -> Sequence[User]:
    stmt = select(User).where(User.balance > min_balance)
    res = await session.scalars(stmt)
    return res.all()


async def add_city(session: AsyncSession, **kwargs) -> CityModel:
    new_obj = await add_object(session, CityModel, **kwargs)
    return new_obj


async def get_city(session: AsyncSession, city_id: int) -> Optional[CityModel]:
    stmt = select(CityModel).where(CityModel.id == city_id)
    res = await session.scalar(stmt)
    return res


async def get_city_by_full_name(session: AsyncSession, full_name: str) -> Optional[CityModel]:
    stmt = select(CityModel).where(CityModel.full_name == full_name)
    res = await session.scalar(stmt)
    return res


async def get_country_cities(session: AsyncSession, country: str) -> Sequence[CityModel]:
    stmt = select(CityModel).where(CityModel.country == country)
    res = await session.scalars(stmt)
    return res.all()


async def add_view(session: AsyncSession, user_id: int, viewer_user_id: int, profile_view=False, phone_view=False) -> \
        Optional[View]:
    stmt = select(
        exists(
            select(View).where(
                View.user_id == user_id,
                View.viewer_user_id == viewer_user_id,
                View.profile_view == profile_view,
                View.phone_view == phone_view,
            )
        )
    )
    exist = await session.scalar(stmt)
    if not exist:
        new_obj = await add_object(
            session, View, user_id=user_id, viewer_user_id=viewer_user_id,
            profile_view=profile_view, phone_view=phone_view
        )
        return new_obj


async def add_sub_types(session: AsyncSession, **kwargs) -> SubscriptionTypeModel:
    new_obj = await add_object(session, SubscriptionTypeModel, **kwargs)
    return new_obj


async def get_sub_types(session: AsyncSession, user_type_id: int = None) -> Union[
    Sequence[SubscriptionTypeModel], SubscriptionTypeModel]:
    if user_type_id:
        stmt = select(SubscriptionTypeModel).where(SubscriptionTypeModel.user_type_id == user_type_id)
        res = await session.scalar(stmt)
        return res
    stmt = select(SubscriptionTypeModel)
    res = await session.scalars(stmt)
    return res.all()


async def get_sub_type(session: AsyncSession, sub_type_id: int) -> Optional[SubscriptionTypeModel]:
    stmt = select(SubscriptionTypeModel).where(SubscriptionTypeModel.id == sub_type_id)
    res = await session.scalar(stmt)
    return res


async def get_sub_type_by_period(session: AsyncSession, period_in_days: int) -> SubscriptionTypeModel:
    stmt = select(SubscriptionTypeModel).where(SubscriptionTypeModel.period_in_days == period_in_days)
    res = await session.scalar(stmt)
    return res


async def get_user_type_by_name(session: AsyncSession, name: str) -> Optional[UserType]:
    stmt = select(UserType).where(UserType.name == name)
    res = await session.scalar(stmt)
    return res


async def get_user_status_by_name(session: AsyncSession, name: str) -> Optional[UserStatus]:
    stmt = select(UserStatus).where(UserStatus.name == name)
    res = await session.scalar(stmt)
    return res


async def add_start_admins(session: AsyncSession):
    config = load_config('.env')
    admin_ids = config.tg_bot.admin_ids
    stmt = update(User).where(User.tg_user_id.in_(admin_ids), is_admin=False)
    res = await session.execute(stmt)
    await session.flush()
    return res.scalars().all()


async def get_bot_settings(session: AsyncSession) -> Optional[BotSettings]:
    stmt = select(BotSettings)
    res = await session.scalar(stmt)
    return res


async def add_start_settings(async_session: async_sessionmaker[AsyncSession]):
    async with async_session() as session:  # type: AsyncSession
        async with session.begin():
            bot_settings = await get_bot_settings(session)
            if bot_settings:
                return bot_settings
            await add_object(
                session, BotSettings,
                terms_of_use_url=consts.TERMS_OF_USE_URL,
                terms_of_use_path=consts.TERMS_OF_USE_FILE_PATH.as_posix(),
                max_profile_photo_count=consts.MAX_PROFILE_PHOTO_COUNT,
                min_days_count_for_change_profile_data=consts.MIN_DAYS_COUNT_FOR_CHANGE_PROFILE_DATA,
                max_about_length=consts.MAX_ABOUT_LENGTH
            )


async def test():
    config = load_config('.env')
    db_config = config.db
    engine = create_async_engine(db_config.create_url())
    async_session = create_session_maker()
    async with engine.begin() as conn:  # type: AsyncConnection
        await conn.run_sync(BaseModel.metadata.create_all)
    async with async_session() as session:  # type: AsyncSession
        async with session.begin():
            # print(await get_object(session, UserData, 1))
            # res = await get_object(session, UserData, 1)
            # print(res.get_reg_kwargs())
            res = await get_sub_types(session)
            print(f"{res=}")
            # print('user status pre', (await res.awaitable_attrs.status).name)
            # sub_type = await get_sub_type(session, 1)
            #
            # print('update_subscription', await res.update_subscription(session, sub_type))
            # # res = await get_user(session, 2223)
            # # print(f"{res=}")
            # # print('user status after', (await res.awaitable_attrs.status).name)


if __name__ == '__main__':
    asyncio.run(test())
