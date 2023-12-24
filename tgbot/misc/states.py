from aiogram.fsm.state import StatesGroup, State


class StatesGroupName(StatesGroup):
    state_name = State()


class GirlRegisterState(StatesGroup):
    start = State()
    full_name = State()
    name = State()
    country = State()
    city = State()
    birthday = State()
    breast_size = State()
    height = State()
    weight = State()
    about = State()
    mobile_phone = State()
    wa = State()
    tg = State()
    photos = State()
    confirm_template = State()
    confirm_photos = State()
    send_check_photo = State()
    confirm_check_photo = State()
    confirm_all = State()


class AdminReviewState(StatesGroup):
    text = State()
    confirm = State()


class BoyState(StatesGroup):
    search_city = State()
