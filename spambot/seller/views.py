from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from spambot.core.models.schemas import SellerView, BaseSeller
from . import crud
from spambot.core.models.db_helper import db_helper
from spambot.Sending_bots.schemas import InputSendingInfo, ViewGetDetailApplicationInfo
from spambot.core.models.seller import Association
from fastapi.responses import StreamingResponse
from spambot.Sending_bots.whatsapp_sending.whatsapp_sender import start_api
import requests
from io import BytesIO
from spambot.Sending_bots.whatsapp_sending.config import BASE_URL
from spambot.Sending_bots.whatsapp_sending.requests_whatsapp_api import (get_chat_messages,
                                                                         get_status_last_message_in_chat)
from spambot.core.config import logger, templates

router = APIRouter(prefix="/request", tags=["Send request"])


@router.post("/create/", response_model=SellerView)
async def create_seller(
        seller_in: BaseSeller,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.create_seller(session=session, seller_in=seller_in)


@router.post("/used_parts/")
async def input_info(
        info: InputSendingInfo,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> None:
    """
    Функция рассылки в whatsapp

    """
    sellers = await crud.get_sellers_where(session=session, type_part=info.application_type,
                                           specialization=info.motorcycle_brand)
    if not sellers:
        raise HTTPException(status_code=400,
                            detail=f"Не найдены поставщики с фирмой мотоцикла {info.motorcycle_brand}")

    for seller in sellers:
        logger.info(f"{seller.name_organization}")
    logger.debug("Запускаем рассылку")
    seller_li = start_api(data=info, sellers=sellers)
    logger.debug("Все сообщения разосланы, создаём заявку!")
    result = await crud.create_applications(session=session, application_info=info)
    create_association = await crud.create_association(application=result,
                                                       seller_li=seller_li,
                                                       session=session)


@router.get("/api/image/")
async def get_api_image():
    image_url = f"{BASE_URL}/screenshot?session=default"

    response = requests.get(image_url)
    image_data = BytesIO(response.content)

    return StreamingResponse(image_data, media_type="image/jpg")


@router.get("/details/{application_id}", response_class=HTMLResponse)
async def get_application_info_by_id(
        application_id: int,
        request: Request,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    data: list[Association] = await crud.get_association(application_id=application_id, session=session)
    if data:
        data_object_li = []
        datetime_create_application = data[0].application.datetime_create
        for element in data:
            answer = get_status_last_message_in_chat(datetime_create_application=datetime_create_application,
                                                     phone_number=element.phone_number)

            object_detail = ViewGetDetailApplicationInfo(application_id=element.applications_id,
                                                         name_organization=element.customer.name_organization,
                                                         phone_number=element.phone_number,
                                                         specialization=element.customer.specialization,
                                                         model_name=element.application.motorcycle_model,
                                                         part_name=element.application.part_name_or_article,
                                                         status_answer=answer)
            data_object_li.append(object_detail)
        return templates.TemplateResponse("detail_application.html", context={"request": request,
                                                                              "data": data_object_li})


@router.delete("/details/delete/{application_id}")
async def delete_application(
        application_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    await crud.delete_application(session=session, application_id=application_id)


@router.delete("/seller/delete/{seller_id}")
async def delete_application(
        seller_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    await crud.delete_seller(session=session, seller_id=seller_id)


@router.get("/details/chat/{phone_number}", response_class=HTMLResponse)
async def get_application_info_by_id(
        phone_number: int,
        request: Request,
):
    data = get_chat_messages(phone_number=phone_number)
    return templates.TemplateResponse("watsapp_chat_api.html", context={"request": request,
                                                                        "data": data})
