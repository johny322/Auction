import abc

from aiogram import Bot
from aiogram.types import PhotoSize

from tgbot.services.telegraph.types import UploadedFile


class FileUploader(abc.ABC):

    async def upload_photo(self, photo: PhotoSize, bot: Bot) -> UploadedFile:
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError
