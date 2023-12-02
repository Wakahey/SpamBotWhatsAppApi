import time

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from spambot.example_templates.schemas import SellerView, BaseSeller
from . import crud
from spambot.core.models.db_helper import db_helper
from spambot.Sending_bots.schemas import InputSendingInfo
from fastapi.responses import StreamingResponse
from spambot.Sending_bots.whatsapp_sending.whatsapp_sender import start_api
import requests
from io import BytesIO
from spambot.Sending_bots.whatsapp_sending.config import BASE_URL
from PIL import Image
import asyncio
from spambot.Sending_bots.whatsapp_sending.requests_whatsapp_api import get_current_status, get_chat_messages
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
):
    sellers = await crud.get_sellers_where(session=session, type_part=info.application_type,
                                           specialization=info.motorcycle_brand)
    time.sleep(2)
    for seller in sellers:
        print(seller.name_organization)

    seller_li = start_api(data=info, sellers=sellers)
    logger.info("Все сообщения разосланы, создаём заявку!")
    result = await crud.create_applications(session=session, application_info=info)
    create_association = await crud.create_association(application=result,
                                                       seller_li=seller_li,
                                                       session=session)


@router.get("/api/image/")
async def get_api_image():
    # Замените URL на URL изображения на другом сайте
    image_url = f"{BASE_URL}/screenshot?session=default"

    # Получаем изображение из другого сайта
    response = requests.get(image_url)
    image_data = BytesIO(response.content)
    # Возвращаем изображение в ответе
    return StreamingResponse(image_data, media_type="image/jpg")


@router.get("/details/{application_id}", response_class=HTMLResponse)
async def get_application_info_by_id(
        application_id: int,
        request: Request,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    data = await crud.get_association(application_id=application_id, session=session)
    data_title = {
        "application_id": data[0].applications_id,
        "brand": data[0].application.motorcycle_brand,
        "model": data[0].application.motorcycle_model,
        "part_name": data[0].application.part_name_or_article,
    }
    return templates.TemplateResponse("detail_application.html", context={"request": request,
                                                                          "data": data,
                                                                          "data_title": data_title})


@router.get("/details/chat/{phone_number}", response_class=HTMLResponse)
async def get_application_info_by_id(
        phone_number: int,
        request: Request,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    data = get_chat_messages(phone_number=phone_number)
    return templates.TemplateResponse("watsapp_chat_api.html", context={"request": request,
                                                                        "data": data})
# @router.websocket("/get_status/")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             # Получите текущий статус
#             status = get_current_status()  # Ваша логика получения статуса
#
#             # Отправьте статус клиенту
#             await websocket.send_json({"status": status})
#
#             # Дождитесь некоторого времени перед отправкой следующего статуса
#             await asyncio.sleep(2)
#     except WebSocketDisconnect:
#         pass

# raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка в данных")
#
#
# @router.get("/", response_model=list[SellerView])
# async def get_sellers(
#         session: AsyncSession = Depends(db_helper.scoped_session_dependency)
# ):
#     return await crud.get_sellers(session=session)
#

# @router.get("/{seller_id}", response_model=SellerView)
# async def get_seller(seller: Seller = Depends(get_seller_by_id)):
#     return seller

# @router.delete("/{seller_id}")
# async def delete_sellers(seller: Seller = Depends(get_seller_by_id),
#                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
#     return await crud.delete_seller(seller=seller, session=session)

# @router.put("/{seller_id}")
# async def update_sellers(seller_update: PartialSeller,
#                          seller: Seller = Depends(get_seller_by_id),
#                          session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
#     return await crud.update_seller_partial(seller=seller,
#                                             session=session,
#                                             seller_update=seller_update)
