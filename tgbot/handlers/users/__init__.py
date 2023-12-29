from aiogram import Router

from .prifile import profile_router
from .cancel_all import cancel_router
from .start import user_router as start_router
from .auction_bets import auction_bets_router

user_router = Router()
user_router.include_router(start_router)
user_router.include_router(profile_router)
user_router.include_router(auction_bets_router)
user_router.include_router(cancel_router)
