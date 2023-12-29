from aiogram import Router

from .bets import bets_router

channels_router = Router()
channels_router.include_router(bets_router)
