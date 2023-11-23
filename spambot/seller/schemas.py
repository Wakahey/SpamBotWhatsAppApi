from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class BaseSeller(BaseModel):
    name_organization: str = Field(..., max_length=20, min_length=3)
    location: str
    associative_words: str


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
