from dataclasses import dataclass
from sys import prefix

# from aiogram.dispatcher.filters.callback_data import CallbackData
from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiohttp import payload


@dataclass
class ProfileMenuCD:
    add_money = 'add_money'
    withdraw_money = 'withdraw_money'
    auction = 'auction'


class YesNoCD(CallbackData, prefix='yn'):
    yes: bool
    no: bool
    payload: Optional[str] = None


class ConfirmCallbackData(CallbackData, prefix="cf"):
    payload: Optional[str] = None
    confirm: bool = True
    extra: Optional[str] = None


class CancelCD(CallbackData, prefix="cancel"):
    payload: Optional[str] = None


class CloseCD(CallbackData, prefix='close'):
    payload: Optional[str] = None


class PaginationCD(CallbackData, prefix="pag"):
    key: str
    page: Optional[int] = None
    payload: Optional[str] = None


class PaymentCD(CallbackData, prefix="payment"):
    payment_type: str
    pay_size: int


class PayoutCD(CallbackData, prefix="payout"):
    payment_type: str


class ConfirmPayoutCD(CallbackData, prefix="c_payout"):
    payout_id: int
    confirm: bool


class PaymentCheckCD(CallbackData, prefix="payment_ch"):
    payment_type: str


class NewBetSizeCD(CallbackData, prefix="new_bet"):
    new_bet: int


agree_agreement = 'agree_agreement'
current_page_callback = 'current_page'
close_payment_type = 'close_payment_type'
close_payment = 'close_payment'
start_auction_cd = 'start_auction'
pay_cancel_cd = 'pay_cancel'
start_auction_payload = 'start_auction'
show_balance_in_chanel_cd = 'show_balance_ic'
user_payout_confirm_payload = 'confirm_payout'
admin_payout_payload = 'a_payout'
admin_mail_payload = 'a_mail'
admin_return_auction_payload = 'a_ret_auction'

disable_advertising_callback = 'disable_adv'
close_advertisement_message = 'close_adv'
