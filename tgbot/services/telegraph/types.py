from __future__ import annotations

from pydantic import Field, BaseModel, field_validator

from tgbot.services.telegraph.config import BASE_TELEGRAPH_API_LINK


class UploadedFile(BaseModel):
    link: str = Field(..., alias="src")

    @field_validator("link")
    def link_validator(cls, value: str):
        return BASE_TELEGRAPH_API_LINK.format(endpoint=value)
