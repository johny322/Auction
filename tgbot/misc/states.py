from aiogram.fsm.state import StatesGroup, State


class Pay(StatesGroup):
    pay_size = State()
    confirm_pay_size = State()
    crypto_bot_check = State()
    anypay_email = State()
    anypay_check = State()


class AuctionStatesGroup(StatesGroup):
    bet_size = State()
    confirm = State()


class PayoutStatesGroup(StatesGroup):
    payout_size = State()
    payout_requisites = State()
    confirm = State()


class Mailing(StatesGroup):
    post = State()
    sure = State()


class AuctionReturnStatesGroup(StatesGroup):
    confirm = State()
