from aiogram import Router
from .common import payment_router
from .anypay import anypay_router
from .crypto_bot import crypto_bot_router

main_payment_router = Router()
main_payment_router.include_router(payment_router)
main_payment_router.include_router(anypay_router)
main_payment_router.include_router(crypto_bot_router)
