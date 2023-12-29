import asyncio
import hashlib
import logging
from dataclasses import dataclass
from enum import Enum, auto
from typing import Literal, Optional

import aiohttp

from tgbot.config import load_config

PAYOUT_TYPES = Literal['qiwi', 'card', 'ym', 'usdt', 'wm', 'mp']

config = load_config()
logger = logging.getLogger('main_logger')


@dataclass
class PaymentMethod:
    qiwi = 'qiwi'
    ym = 'ym'
    wm = 'wm'
    card = 'card'
    advcash = 'advcash'
    pm = 'pm'
    applepay = 'applepay'
    googlepay = 'googlepay'
    samsungpay = 'samsungpay'
    sbp = 'sbp'
    payeer = 'payeer'
    btc = 'btc'
    eth = 'eth'
    bch = 'bch'
    ltc = 'ltc'
    dash = 'dash'
    zec = 'zec'
    doge = 'doge'
    usdt = 'usdt'
    mts = 'mts'
    beeline = 'beeline'
    megafon = 'megafon'
    tele2 = 'tele2'
    term = 'term'


@dataclass
class Currency:
    RUB = 'RUB'
    UAH = 'UAH'
    BYN = 'BYN'
    KZT = 'KZT'
    USD = 'USD'
    EUR = 'EUR'


class CreatePayStatus(str, Enum):
    ok = auto()
    error = auto()


class PayStatus(str, Enum):
    ok = auto()
    error = auto()
    no_pay = auto()
    no_transaction = auto()


class NoExchangeRate(Exception):
    pass


class AnyPay:

    def __init__(self, debug=False):
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'multipart/form-data'
        }
        self.__project_id = config.payments.anypay_project_id

        self.__api_id = config.payments.anypay_api_id
        self.__api_key = config.payments.anypay_api_key

        self.__api_url = f'https://anypay.io/api/{{method}}/{self.__api_id}'

    @staticmethod
    def _get_sign(value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()

    async def _get_response(self, url, params=None) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url,
                    headers=self.headers,
                    params=params
            ) as resp:
                return await resp.json()

    async def balance(self):
        url = self.__api_url.format(
            method='balance',
        )
        params = dict(
            sign=self._get_sign(f'balance{self.__api_id}{self.__api_key}')
        )
        return await self._get_response(url, params)

    async def _create_payment(self, project_id: int, pay_id: int, amount: int,
                              currency: str, desc: str, method: str, email: str):
        # {
        #   "result": {
        #     "transaction_id": 17568677,
        #     "pay_id": 1,
        #     "status": "waiting",
        #     "payment_url": "https://anypay.io/payment/40410b85-3998-4bf8-9777-e410d597f457"
        #   }
        # }
        url = self.__api_url.format(
            method='create-payment'
        )
        sign = f'create-payment{self.__api_id}{project_id}{pay_id}{amount}{currency}{desc}{method}{self.__api_key}'
        sign = self._get_sign(sign)
        params = dict(
            project_id=project_id,
            pay_id=pay_id,
            amount=amount,
            currency=currency,
            desc=desc,
            method=method,
            email=email,
            sign=sign
        )
        res = await self._get_response(url, params)
        return res

    async def _payments(self, project_id: int, trans_id: Optional[int] = None, offset: Optional[int] = None):
        url = self.__api_url.format(
            method='payments'
        )

        sign = f'payments{self.__api_id}{project_id}{self.__api_key}'
        sign = self._get_sign(sign)
        params = dict(
            project_id=project_id,
            sign=sign
        )
        if trans_id:
            params['trans_id'] = trans_id
        if offset:
            params['offset'] = offset

        res = await self._get_response(url, params)
        # print(res)
        # {
        #     "result": {
        #         "payments": {
        #             "17568677": {
        #                 "transaction_id": 17568677,
        #                 "pay_id": 1,
        #                 "status": "waiting",
        #                 "method": "card",
        #                 "amount": 10,
        #                 "currency": "rub",
        #                 "profit": 10,
        #                 "email": "is.boldyrev@yandex.ru",
        #                 "desc": "Тест api",
        #                 "date": "15.03.2023 00:07:22",
        #                 "complete_date": ""
        #             }
        #         }
        #     }
        # }
        return res

    async def _get_new_pay_id(self, project_id: int) -> int:
        payments_res = await self._payments(
            project_id=project_id,
        )
        payments: Optional[dict] = payments_res['result']['payments']
        if not payments:
            new_pay_id = 1
        else:
            last_transaction_id: str = list(payments.keys())[0]
            last_pay_id = payments[last_transaction_id]['pay_id']
            new_pay_id = last_pay_id + 1
        return new_pay_id

    async def create(self, amount: int, desc: str, method: str, email: str):
        project_id = self.__project_id
        pay_id = await self._get_new_pay_id(project_id)
        create_payment_res = await self._create_payment(
            project_id=project_id,
            pay_id=pay_id,
            amount=amount,
            currency=Currency.RUB,
            desc=desc,
            method=method,
            email=email
        )
        if 'error' in create_payment_res:
            logger.warning(create_payment_res)
            return CreatePayStatus.error
        try:
            result = create_payment_res['result']
        except KeyError:
            logger.warning(create_payment_res)
            return CreatePayStatus.error
        transaction_id = result['transaction_id']
        status = result['status']
        if status != 'waiting':
            logger.warning(create_payment_res)
            return CreatePayStatus.error
        payment_url = result['payment_url']
        return CreatePayStatus.ok, transaction_id, payment_url

    async def check_payment(self, trans_id: int) -> PayStatus:
        payments_res = await self._payments(
            project_id=self.__project_id,
            trans_id=trans_id
        )
        if 'error' in payments_res:
            logger.warning(payments_res)
            return PayStatus.error
        try:
            transaction_data = payments_res['result']['payments'][str(trans_id)]
        except KeyError:
            logger.warning(payments_res)
            return PayStatus.no_transaction
        status = transaction_data['status']
        if status != 'paid':
            return PayStatus.no_pay
        else:
            return PayStatus.ok


async def test():
    ap = AnyPay()
    # await ap.create_payment(
    #     project_id=1,
    #     pay_id=1,
    #     amount=10,
    #     currency='RUB',
    #     desc='Тест api',
    #     method='card',
    #     email='is.boldyrev@yandex.ru'
    # )
    # {
    #   "result": {
    #     "transaction_id": 17568677,
    #     "pay_id": 1,
    #     "status": "waiting",
    #     "payment_url": "https://anypay.io/payment/40410b85-3998-4bf8-9777-e410d597f457"
    #   }
    # }
    # await ap.balance()
    # await ap.payments(
    #     project_id=1,
    # )
    # print(await ap._get_new_pay_id(project_id=1))
    # res = await ap.create(
    #     amount=10,
    #     desc='Тест api',
    #     method=PaymentMethod.card,
    #     email=''
    # )
    res = await ap.check_payment(
        trans_id=17570977
    )
    print(res)


if __name__ == '__main__':
    asyncio.run(test())
