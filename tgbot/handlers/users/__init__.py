from aiogram import Router

from .cancel_all import cancel_router
from .start import user_router as start_router

user_router = Router()
user_router.include_router(start_router)
user_router.include_router(cancel_router)
