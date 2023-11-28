from pydantic import BaseModel, Field, ConfigDict, EmailStr, validator
from datetime import datetime
from typing import Union


class BaseSeller(BaseModel):
    name_organization: str = Field(..., max_length=30, min_length=3)
    location: str
    associative_words: str
    customer_type: str


class SellerView(BaseSeller):
    id: int
    date_add: datetime


class CreateSeller(BaseSeller):
    pass


class UpdateSeller(BaseSeller):
    pass


class PartialSeller(BaseSeller):
    name_organization: str | None = None
    location: str | None = None
    associative_words: str | None = None


class Seller(SellerView):
    model_config = ConfigDict(from_attributes=True)


class SocialNetwork(BaseModel):
    telegram_url: str = None
    vk_url: str = None
    email: str = None
    phone_number: str = None


class SellerSocial(BaseSeller):
    social_network: SocialNetwork | None


class SellerSocialResponse(SellerSocial):
    id: int
    date_add: datetime
