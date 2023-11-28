from pydantic import BaseModel, Field


class InputSendingInfo(BaseModel):
    seller_type: str
    sending_type: str
    part_number: str | None
    email_subject: str = Field(..., min_length=5, max_length=35)
    email_body: str = Field(..., min_length=15)
