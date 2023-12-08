# -*- coding: utf-8 -*-
import time

import vk_api
from spambot.Sending_bots.vk_api_sending.config import TOKEN, BASE_MESSAGE, COUNT_MESSAGE
from spambot.core.config import logger
from spambot.Sending_bots.schemas import InputSendingInfo
from spambot.core.models.seller import WholesaleCustomer
from datetime import datetime
from fastapi.exceptions import HTTPException


def authorization_token():
    session_vk = vk_api.VkApi(token=TOKEN)
    vk = session_vk.get_api()
    return vk


def get_my_information(vk_func):
    try:
        user_info = vk_func.users.get()
        return int(user_info[0]["id"]), " ".join([user_info[0]["first_name"], user_info[0]["last_name"]])
    except vk_api.exceptions.ApiError as exc:
        raise HTTPException(status_code=404, detail="Проблема с Вконтакте (возможно ввёден не верный токен, или "
                                                    "сайт не работает, или ещё что-нибудь). Сообщите айтишнику!.")


def get_status_last_vk_messages(vk_id, vk_func=authorization_token()):
    logger.info(f"Получаем последнее сообщение с VK id: {vk_id}")
    history_chat = vk_func.messages.getHistory(user_id=vk_id, count=1)
    my_id, my_name = get_my_information(vk_func)
    if history_chat["items"][0]["from_id"] == my_id:
        return False
    else:
        answer = history_chat["items"][0]["text"]
        return answer


def get_chat_message_all(vk_id, vk_func=authorization_token()):
    history_chat = vk_func.messages.getHistory(user_id=vk_id, count=COUNT_MESSAGE, rev=0)
    my_id, my_name = get_my_information(vk_func)
    data_message = []
    for message in history_chat["items"]:
        if message["from_id"] == my_id:
            data_message.append({"name": "МотоДвиж",
                                 "body": message["text"],
                                 "time": datetime.fromtimestamp(message["date"])
                                 })
        elif message["from_id"] != my_id:
            data_message.append(
                {"phone_number": (message["from_id"]),
                 "body": message["text"],
                 "time": datetime.fromtimestamp(message["date"])
                 })

    return data_message[::-1]


def get_info_by_id(id_num, vk_auth=authorization_token()):
    logger.info(f"Получаем информацию по id={id_num}")
    user = vk_auth.users.get(user_ids=f"{id_num}")
    if user:
        logger.info(user)
        id_num = user[0]["id"]
        return id_num
    else:
        logger.error("Пользователя с таким id не существует")
        raise ValueError("Пользователя с таким id не существует")


def send_message(info: InputSendingInfo, sellers: list[WholesaleCustomer], vk_func):
    association_li = []
    for seller in sellers:
        try:
            vk_func.messages.send(user_id=seller.vk_id,
                                  random_id=0,
                                  message=BASE_MESSAGE.format(info.motorcycle_brand,
                                                              info.motorcycle_model,
                                                              info.manufacturing_year,
                                                              info.vin_number,
                                                              info.part_name_or_article,
                                                              info.additional_info))
            association_li.append(seller)

        except vk_api.exceptions.ApiError as exc:
            logger.error(f"Пользователю с id: {id} нельзя отправить сообщение\n"
                         f"(вероятно закрыты личные сообщения)")
        time.sleep(0.5)
    return association_li


def start_api_vk_sending(info: InputSendingInfo, sellers: list[WholesaleCustomer]):
    logger.info("Авторизация токена")
    vk_func = authorization_token()
    my_id, my_first_last_name = get_my_information(vk_func=vk_func)
    logger.info(f"Активный аккаунт:\nID:{my_id}\nИмя: {my_first_last_name}")
    logger.info("Запускаем рассылку Вконтакте")
    seller_li = send_message(info=info, sellers=sellers, vk_func=vk_func)
    return seller_li


if __name__ == '__main__':
    start_api_vk_sending()
