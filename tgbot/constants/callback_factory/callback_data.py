from sys import prefix

# from aiogram.dispatcher.filters.callback_data import CallbackData
from typing import Optional

from aiogram.filters.callback_data import CallbackData
from aiohttp import payload


class ConfirmCallbackData(CallbackData, prefix="cf"):
    payload: Optional[str] = None
    confirm: bool = True
    extra: Optional[str] = None


class ConfirmRegCallbackData(CallbackData, prefix="cf_reg"):
    payload: Optional[str] = None
    confirm: bool = True


class BuySubCD(CallbackData, prefix="buy_sub"):
    sub_type_id: Optional[int] = None


class CancelCD(CallbackData, prefix="cancel"):
    payload: Optional[str] = None


class CloseCD(CallbackData, prefix='close'):
    payload: Optional[str] = None


class PaginationCD(CallbackData, prefix="pag"):
    key: str
    page: Optional[int] = None
    payload: Optional[str] = None


class ShowPhoneNumberCD(CallbackData, prefix="show_phone"):
    db_user_id: int  # id модели в бд


class BuyPhoneNumberCD(CallbackData, prefix="buy_phone"):
    user_id: int  # id модели в бд
    city_id: int
    page: int  # номер страницы для создания клавиатуры с пагинацией


class PaymentCD(CallbackData, prefix="payment"):
    payment_type: str
    period_in_days: int
    price: float
    currency: str
    status_id: int


class InvoicePayload(CallbackData, prefix="iv"):
    days: int
    old_message_id: int


agree_agreement = 'agree_agreement'
cancel_search = 'cancel_search'
current_page_callback = 'current_page'
show_phone_number_callback = 'show_phone_number_callback'
close_sup_type = 'close_sup_type'
close_payment_type = 'close_payment_type'
close_payment = 'close_payment'
account_statistics_cd = 'account_statistics'
close_profile_info = 'close_profile_info'
change_account_data_cd = 'change_account_data'
