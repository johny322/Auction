import asyncio
import platform
from dataclasses import dataclass
from typing import Literal, Union, List, Optional, Tuple

import aiohttp

from tgbot.config import load_config

config = load_config()

supported_assets = ['BTC', 'ETH', 'TON', 'BNB', 'USDT']
asset_type = Literal['BTC', 'ETH', 'TON', 'BNB', 'USDT']


class NoExchangeRate(Exception):
    pass


class CryptoBot:

    def __init__(self, debug=False):
        self.headers = {
            'Crypto-Pay-API-Token': config.payments.crypto_bot_token
        }
        if debug or platform.system() == 'Windows':
            self.__api_url = 'https://testnet-pay.crypt.bot/api/'
        else:
            self.__api_url = 'https://pay.crypt.bot/api/'
        self.supported_assets = supported_assets

    async def _get_response(self, url, params=None) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url,
                    headers=self.headers,
                    params=params
            ) as resp:
                return await resp.json()

    async def getMe(self):
        url = self.__api_url + 'getMe'
        return await self._get_response(url)

    async def createInvoice(self, asset: asset_type, amount: Union[float, int], description: str = None,
                            paid_btn_name: str = None, paid_btn_url: str = None, allow_comments='false') -> dict:
        # {'ok': True, 'result': {'invoice_id': 21937, 'status': 'active', 'hash': 'IVhVSz7SevLr', 'asset': 'USDT', 'amount': '1', 'pay_url': 'https://t.me/CryptoTestnetBot?start=IVhVSz7SevLr', 'created_at': '2022-11-22T11:15:14.156Z', 'allow_comments': True, 'allow_anonymous': True}}
        url = self.__api_url + 'createInvoice'
        params = dict(amount=amount, asset=asset, allow_comments=allow_comments)
        if description:
            params['description'] = description
        if paid_btn_name:
            params['paid_btn_name'] = paid_btn_name
        if paid_btn_url:
            params['paid_btn_url'] = paid_btn_url

        return await self._get_response(url, params)

    async def getInvoices(self, asset: str = None, invoice_ids: str = None, status: str = None, offset: str = None,
                          count: int = None) -> dict:
        # {'ok': True, 'result': {'items': [{'invoice_id': 21937, 'status': 'paid', 'hash': 'IVhVSz7SevLr', 'asset': 'USDT', 'amount': '1', 'pay_url': 'https://t.me/CryptoTestnetBot?start=IVhVSz7SevLr', 'created_at': '2022-11-22T11:15:14.156Z', 'allow_comments': True, 'allow_anonymous': True, 'paid_at': '2022-11-22T14:57:48.169Z', 'paid_anonymously': False}]}}
        url = self.__api_url + 'getInvoices'
        params = {}
        if asset:
            params['asset'] = asset
        if invoice_ids:
            params['invoice_ids'] = invoice_ids
        if status:
            params['status'] = status
        if offset:
            params['offset'] = offset
        if count:
            params['count'] = count

        return await self._get_response(url, params)

    async def getExchangeRates(self) -> dict:
        # {'ok': True, 'result': [{'is_valid': True, 'source': 'USDT', 'target': 'RUB', 'rate': '60.44000000'}, {'is_valid': True, 'source': 'USDT', 'target': 'USD', 'rate': '0.99902200'}]}
        url = self.__api_url + 'getExchangeRates'
        return await self._get_response(url)

    async def getCurrencies(self) -> dict:
        url = self.__api_url + 'getCurrencies'
        return await self._get_response(url)

    async def exchange_currency(self, source_currency: str, source_amount: int, target_currency: str = 'RUB') -> \
            Optional[Tuple[float, float]]:
        res = await self.getExchangeRates()
        all_exchange_data: List[dict] = res['result']
        for exchange_data in all_exchange_data:
            if exchange_data['source'] == source_currency and exchange_data['target'] == target_currency:
                rate = float(exchange_data['rate'])
                return round(rate * source_amount, 2), rate

    async def rub_to_currency(self, rub_amount: int, target_currency: str) -> \
            Optional[Tuple[float, float]]:
        res = await self.getExchangeRates()
        all_exchange_data: List[dict] = res['result']
        for exchange_data in all_exchange_data:
            if exchange_data['source'] == target_currency and exchange_data['target'] == 'RUB':
                rate = float(exchange_data['rate'])
                return round(rub_amount / rate, 2), rate
        return 0, 0

    async def create(self, asset: asset_type, amount: Union[float, int], description: str = None,
                     paid_btn_name: str = None, paid_btn_url: str = None) -> Tuple[int, str, float]:
        """

        :param asset:
        :param amount: цена в рублях
        :param description:
        :param paid_btn_name:
        :param paid_btn_url:
        :return: (21999, 'https://t.me/CryptoTestnetBot?start=IVVOWIF8PtJC')
        """
        if not paid_btn_name:
            paid_btn_name = 'openBot'
            paid_btn_url = config.tg_bot.bot_link()
            description = f'Пополнение баланса в боте @{config.tg_bot.bot_username} на {amount} RUB'
        new_amount, exchange_rate = await self.rub_to_currency(amount, asset)
        if not new_amount:
            raise NoExchangeRate
        invoice = await self.createInvoice(asset, new_amount, description, paid_btn_name, paid_btn_url)
        invoice_result: dict = invoice['result']
        return invoice_result.get('invoice_id'), invoice_result.get('pay_url'), exchange_rate

    async def check_payment(self, invoice_id: Union[int, str]) -> bool:
        invoices_data = await self.getInvoices(invoice_ids=invoice_id)
        result: list = invoices_data['result']['items']
        if result:
            invoice_data = result[0]
            if invoice_data.get('status') == 'paid':
                return True
        return False


#
# @dataclass
# class CryptoBotPayment:
#     asset: asset_type = None
#     amount: Union[float, int] = None
#     description: str = None
#     paid_btn_name: str = None
#     paid_btn_url: str = None
#     _bot_api = CryptoBot()
#     _invoice_id: int = None
#
#     async def create(self):
#         invoice = await self._bot_api.createInvoice(
#             self.asset,
#             self.amount,
#             self.description,
#             self.paid_btn_name,
#             self.paid_btn_url
#         )
#         self._invoice_id = invoice['result']['invoice_id']
#
#     async def check_payment(self):
#         invoice_id = self._invoice_id
#         invoices_data = await self._bot_api.getInvoices(invoice_ids=invoice_id)
#         result: list = invoices_data['result']['items']
#         if result:
#             invoice_data = result[0]
#             if invoice_data.get('status') == 'paid':
#                 return True
#         raise NoPaymentFound


async def test():
    cb = CryptoBot()
    res = await cb.getMe()
    print(res)


if __name__ == '__main__':
    asyncio.run(test())
