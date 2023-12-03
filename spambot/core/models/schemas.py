from pydantic import BaseModel, Field, ConfigDict, EmailStr, validator
from datetime import datetime
from typing import Union


class BaseSeller(BaseModel):
    name_organization: str = Field(..., max_length=30, min_length=3)
    type_part: str
    specialization: str
    location: str
    whatsapp: str
    email: str

    @validator("whatsapp")
    def validate_whatsapp(cls, value):
        if not value.startswith("7") or len(value) != 11 or not value.isdigit():
            raise ValueError("Некорректный номер WhatsApp. Номер должен начинаться с '7' и иметь 11 цифр.")
        return value


class SellerView(BaseSeller):
    id: int
    date_add: datetime


class Seller(BaseSeller):
    model_config = ConfigDict(from_attributes=True)
