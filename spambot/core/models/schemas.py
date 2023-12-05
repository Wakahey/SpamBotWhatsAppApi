from pydantic import BaseModel, Field, ConfigDict, EmailStr, validator
from datetime import datetime
from typing import Union
from spambot.Sending_bots.vk_api_sending.api_func import get_info_by_id


class BaseSeller(BaseModel):
    name_organization: str = Field(...)
    type_part: str
    specialization: str
    location: str
    whatsapp: str | None
    vk_id: int | str | None
    email: str

    @validator("whatsapp")
    def validate_whatsapp(cls, value):
        if value:
            if not value.startswith("7") or len(value) != 11 or not value.isdigit():
                raise ValueError("Некорректный номер WhatsApp. Номер должен начинаться с '7' и иметь 11 цифр.")
        return value

    @validator("vk_id")
    def validate_vk_id(cls, value):
        if value:
            id_num = get_info_by_id(id_num=value)
            return id_num
        return value


class SellerView(BaseSeller):
    id: int
    date_add: datetime


class Seller(BaseSeller):
    model_config = ConfigDict(from_attributes=True)
