import asyncio
import os
import secrets
from io import BytesIO
from typing import Optional

import aiohttp
from aiogram import Bot
from aiogram.types import PhotoSize

from tgbot.services.telegraph.abstract import FileUploader
from tgbot.services.telegraph.config import BASE_TELEGRAPH_API_LINK
from tgbot.services.telegraph.exceptions import TelegraphAPIError
from tgbot.services.telegraph.types import UploadedFile


class TelegraphService(FileUploader):
    def __init__(self) -> None:
        self._session: Optional[aiohttp.ClientSession] = None

    async def upload_photo(self, photo: PhotoSize, bot: Bot) -> UploadedFile:
        form = aiohttp.FormData(quote_fields=False)
        file_id = photo.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        downloaded_photo: BytesIO = await bot.download_file(file_path)

        form.add_field(secrets.token_urlsafe(8), downloaded_photo)

        session = await self.get_session()
        response = await session.post(
            BASE_TELEGRAPH_API_LINK.format(endpoint="upload"),
            data=form
        )
        if not response.ok:
            raise TelegraphAPIError(
                "Something went wrong, response from telegraph is not successful. "
                f"Response: {response}"
            )
        json_response = await response.json()
        return [UploadedFile.parse_obj(obj) for obj in json_response][0]

    async def upload_photo_by_file_id(self, file_id: str, bot: Bot) -> UploadedFile:
        form = aiohttp.FormData(quote_fields=False)
        file = await bot.get_file(file_id)
        file_path = file.file_path
        downloaded_photo: BytesIO = await bot.download_file(file_path)

        form.add_field(secrets.token_urlsafe(8), downloaded_photo)

        session = await self.get_session()
        response = await session.post(
            BASE_TELEGRAPH_API_LINK.format(endpoint="upload"),
            data=form
        )
        if not response.ok:
            raise TelegraphAPIError(
                "Something went wrong, response from telegraph is not successful. "
                f"Response: {response}"
            )
        json_response = await response.json()
        return [UploadedFile.parse_obj(obj) for obj in json_response][0]

    async def upload_photo_by_bytes(self, downloaded_photo: bytes) -> UploadedFile:
        form = aiohttp.FormData(quote_fields=False)
        form.add_field(secrets.token_urlsafe(8), downloaded_photo)

        session = await self.get_session()
        response = await session.post(
            BASE_TELEGRAPH_API_LINK.format(endpoint="upload"),
            data=form
        )
        if not response.ok:
            raise TelegraphAPIError(
                "Something went wrong, response from telegraph is not successful. "
                f"Response: {response}"
            )
        json_response = await response.json()
        return [UploadedFile.parse_obj(obj) for obj in json_response][0]

    async def upload_photo_by_file_path(self, file_path: str) -> UploadedFile:
        form = aiohttp.FormData(quote_fields=False)
        with open(file_path, 'rb') as f:
            downloaded_photo = f.read()
        form.add_field(secrets.token_urlsafe(8), downloaded_photo)

        session = await self.get_session()
        response = await session.post(
            BASE_TELEGRAPH_API_LINK.format(endpoint="upload"),
            data=form
        )
        if not response.ok:
            raise TelegraphAPIError(
                "Something went wrong, response from telegraph is not successful. "
                f"Response: {response}"
            )
        json_response = await response.json()
        return [UploadedFile.parse_obj(obj) for obj in json_response][0]

    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            new_session = aiohttp.ClientSession()
            self._session = new_session
        return self._session

    async def close(self) -> None:
        if self._session is None:
            return None
        await self._session.close()


async def test():
    ts = TelegraphService()
    await ts.get_session()
    path = r'E:\Python practice\Tg bots\Mem bot\photos\ЧТО ЗА МЕМ. Электронная версия'
    links = []
    for i in os.listdir(path):
        i_path = os.path.join(path, i)
        print(os.path.abspath(i_path))
        r = await ts.upload_photo_by_file_path(i_path)
        print(r)
        links.append(r.link)
        await asyncio.sleep(0.05)
    await ts.close()
    print(links)


if __name__ == '__main__':
    asyncio.run(test())
