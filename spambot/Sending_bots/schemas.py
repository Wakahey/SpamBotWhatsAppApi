from pydantic import BaseModel, Field
from datetime import datetime


class InputSendingInfo(BaseModel):
    motorcycle_brand: str = Field(..., )
    motorcycle_model: str
    part_name_or_article: str
    additional_info: str | None
    application_type: str


class ViewGetDetailApplicationInfo:
    def __init__(self, application_id, name_organization,
                 phone_number, specialization, model_name,
                 part_name, status_answer=None):
        self.application_id: int = application_id
        self.name_organization: str = name_organization
        self.phone_number: int = phone_number
        self.specialization: str = specialization
        self.model_name: str = model_name
        self.part_name: str = part_name
        self.status_answer: str = status_answer
