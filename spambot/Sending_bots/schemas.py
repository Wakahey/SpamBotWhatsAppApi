from pydantic import BaseModel, Field


class InputSendingInfo(BaseModel):
    motorcycle_brand: str = Field(..., )
    motorcycle_model: str
    part_name_or_article: str
    additional_info: str | None
    application_type: str
