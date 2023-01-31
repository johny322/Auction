from aiogram.dispatcher.filters.callback_data import CallbackData


class CallbackFactory(CallbackData, prefix="prefix"):
    action: str
    name: str
