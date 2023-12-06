# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from spambot.core.models.schemas import SellerView, BaseSeller
from . import crud
from spambot.core.models.db_helper import db_helper
from spambot.Sending_bots.schemas import InputSendingInfo, ViewGetDetailVK, ViewGetDetailWhatsApp
from spambot.core.models.seller import Association
from fastapi.responses import StreamingResponse
from spambot.Sending_bots.whatsapp_sending.whatsapp_sender import start_api
import requests
from io import BytesIO
from spambot.Sending_bots.whatsapp_sending.config import BASE_URL
from spambot.Sending_bots.whatsapp_sending.requests_whatsapp_api import (get_chat_messages,
                                                                         get_status_last_message_in_chat)
from spambot.core.config import logger, templates
from spambot.Sending_bots.vk_api_sending.api_func import (start_api_vk_sending,
                                                          get_status_last_vk_messages,
                                                          get_chat_message_all)

router = APIRouter(prefix="/request", tags=["Send request"])


@router.post("/create/", response_model=SellerView)
async def create_seller(
        seller_in: BaseSeller,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.create_seller(session=session, seller_in=seller_in)


@router.get("/get_models/{brand}")
async def get_models_moto(brand: str,
                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_moto_model(session=session, brand=brand)


@router.post("/used_parts/")
async def input_info(
        info: InputSendingInfo,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> None:
    """
    Функция рассылки в whatsapp и вконтакте

    """
    if info.social_network == "WhatsApp":
        sellers = await crud.get_sellers_where(session=session, info=info)
        if not sellers:
            raise HTTPException(status_code=400,
                                detail=f"Не найдены поставщики с фирмой мотоцикла {info.motorcycle_brand}")

        for seller in sellers:
            logger.info(f"(Проверка){seller.name_organization}")
        logger.debug("Запускаем рассылку WhatsApp")
        seller_li = start_api(data=info, sellers=sellers)
        logger.debug("Все сообщения WhatsApp разосланы, создаём заявку!")
        result = await crud.create_applications(session=session, application_info=info)
        create_association = await crud.create_association(application=result,
                                                           seller_li=seller_li,
                                                           session=session)
    elif info.social_network == "Вконтакте":
        sellers = await crud.get_sellers_where(session=session, info=info)
        if not sellers:
            raise HTTPException(status_code=400,
                                detail=f"Не найдены поставщики с фирмой мотоцикла {info.motorcycle_brand}")
        for seller in sellers:
            logger.info(f"(Проверка){seller.name_organization}")
        logger.debug("Запускаем рассылку Вконтакте")
        seller_li = start_api_vk_sending(info=info, sellers=sellers)
        logger.debug("Все сообщения Вконтакте разосланы, создаём заявку!")
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
        application_data = data[0].application
        data_object_li = []
        if application_data.social_network == "WhatsApp":
            for element in data:
                answer = get_status_last_message_in_chat(phone_number=element.customer.whatsapp)

                object_detail = ViewGetDetailWhatsApp(application_id=element.applications_id,
                                                      name_organization=element.customer.name_organization,
                                                      phone_number=element.customer.whatsapp,
                                                      specialization=element.customer.specialization,
                                                      model_name=element.application.motorcycle_model,
                                                      part_name=element.application.part_name_or_article,
                                                      status_answer=answer)
                data_object_li.append(object_detail)
        elif application_data.social_network == "Вконтакте":
            for element in data:
                answer = get_status_last_vk_messages(vk_id=element.customer.vk_id)

                object_detail = ViewGetDetailVK(application_id=element.applications_id,
                                                name_organization=element.customer.name_organization,
                                                vk_id=element.customer.vk_id,
                                                specialization=element.customer.specialization,
                                                model_name=element.application.motorcycle_model,
                                                part_name=element.application.part_name_or_article,
                                                status_answer=answer)
                data_object_li.append(object_detail)
    else:
        return 404

    return templates.TemplateResponse("detail_application.html", context={"request": request,
                                                                          "data": data_object_li,
                                                                          "application_data": application_data})


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


@router.get("/details/chat_whatsapp/{phone_number}", response_class=HTMLResponse)
async def get_application_info_by_id(
        phone_number: int,
        request: Request,
):
    data = get_chat_messages(phone_number=phone_number)
    app_type = "WhatsApp"
    return templates.TemplateResponse("chat_api.html", context={"request": request,
                                                                "data": data,
                                                                "app_type": app_type})


@router.get("/details/chat_vk/{vk_id}", response_class=HTMLResponse)
async def get_application_info_by_id(
        vk_id: int,
        request: Request,
):
    data = get_chat_message_all(vk_id=vk_id)
    app_type = "Вконтакте"
    return templates.TemplateResponse("chat_api.html", context={"request": request,
                                                                "data": data,
                                                                "app_type": app_type})
