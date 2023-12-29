import enum
from typing import Tuple

from aiogram import Bot
from aiogram.utils.text_decorations import html_decoration
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot import texts
from tgbot.config import Config
from tgbot.constants.consts import PAYOUT_MIN_SUM_FOR_ALERT
from tgbot.db import db_commands
from tgbot.db.models import PayoutMethod, PayoutStatus, User, Payout
from tgbot.keyboards import inline


class PayoutResult(enum.Enum):
    no_balance = 0
    good = 1


class PayoutLogic:
    def __init__(self, bot: Bot, config: Config, session: AsyncSession):
        self.bot = bot
        self.config = config
        self.session = session

    async def _send_message_to_admin(self, text: str, payout_id: int):
        await self.bot.send_message(
            chat_id=self.config.tg_bot.admin_ids[0],
            text=text,
            reply_markup=inline.confirm_payout_keyboard_inline(payout_id)
        )

    async def _add_payout(self, to_user_id: int, payout_sum: int, payout_method: PayoutMethod) -> int:
        payout = await db_commands.add_payout(
            self.session,
            to_user_id=to_user_id,
            payout_sum=payout_sum,
            payout_method=payout_method,
            status=PayoutStatus.processing.value
        )
        return payout.id

    async def create_payout(self, text: str, to_user_id: int, payout_sum: int, payout_method: PayoutMethod):
        payout_id = await self._add_payout(to_user_id, payout_sum, payout_method)
        await self._send_message_to_admin(text, payout_id)

    async def confirm_payout(self, text: str, payout_id: int) -> Tuple[PayoutResult, Payout]:
        payout = await db_commands.get_payout(self.session, payout_id)
        to_user: User = await payout.awaitable_attrs.to_user
        if to_user.balance < payout.payout_sum:
            return PayoutResult.no_balance, payout
        await db_commands.update_payout(
            self.session, payout_id,
            status=PayoutStatus.completed.value
        )
        await db_commands.update_user_by_db_id(
            self.session, to_user.id,
            balance=to_user.balance - payout.payout_sum,
            paid_balance=to_user.paid_balance + payout.payout_sum
        )
        await self.bot.send_message(
            chat_id=to_user.tg_user_id,
            text=text.format(payout.payout_sum)
        )
        if payout.payout_sum >= PAYOUT_MIN_SUM_FOR_ALERT:
            chanel_text = texts.good_payout_chanel_message_text.format(
                full_name=html_decoration.quote(to_user.full_name),
                username=to_user.username,
                payout_sum=payout.payout_sum,
                status='успешно'
            )
            await self.bot.send_message(
                chat_id=self.config.tg_bot.payout_chanel_id,
                text=chanel_text
            )
        return PayoutResult.good, payout
