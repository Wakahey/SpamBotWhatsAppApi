from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum
from fastapi.exceptions import HTTPException


class InputSendingInfo(BaseModel):
    motorcycle_brand: str = Field(..., )
    motorcycle_model: str
    manufacturing_year: str
    vin_number: str
    part_name_or_article: str
    social_network: str = Field(...)
    additional_info: str | None
    application_type: str

    @validator("social_network")
    def validate_social_network(cls, value):
        valid_social_networks = {"Вконтакте", "WhatsApp"}
        if value not in valid_social_networks:
            raise HTTPException(status_code=400, detail="Выберите в какой мессенджер будем отправлять")
        return value


class ViewGetDetailApplicationInfo:
    def __init__(self, application_id, name_organization,
                 specialization, model_name,
                 part_name, status_answer=None):
        self.application_id: int = application_id
        self.name_organization: str = name_organization
        self.specialization: str = specialization
        self.model_name: str = model_name
        self.part_name: str = part_name
        self.status_answer: str = status_answer


class ViewGetDetailWhatsApp(ViewGetDetailApplicationInfo):
    def __init__(self, application_id, name_organization,
                 specialization, model_name,
                 part_name, status_answer=None, phone_number=None):
        super().__init__(application_id, name_organization, specialization, model_name, part_name, status_answer)
        self.phone_number: str = phone_number


class ViewGetDetailVK(ViewGetDetailApplicationInfo):
    def __init__(self, application_id, name_organization,
                 specialization, model_name,
                 part_name, status_answer=None, vk_id=None):
        super().__init__(application_id, name_organization, specialization, model_name, part_name, status_answer)
        self.vk_id: int = vk_id
