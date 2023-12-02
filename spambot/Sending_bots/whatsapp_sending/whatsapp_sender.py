from spambot.Sending_bots.whatsapp_sending.docker_run_api import (is_container_running,
                                                                  start_docker_container)
import time
from spambot.core.config import logger
import threading
from spambot.Sending_bots.whatsapp_sending import requests_whatsapp_api
from spambot.core.models.seller import WholesaleCustomer, Applications


def start_container():
    image_name = "devlikeapro/whatsapp-http-api:latest"
    if not is_container_running(image_name=image_name):
        logger.debug("Контейнер не запущен, попытка запуска")
        start_docker = threading.Thread(target=start_docker_container)
        start_docker.start()
        time.sleep(4)
        if is_container_running(image_name):
            logger.info("Контейнер успешно запущен!")
            time.sleep(1)
            if requests_whatsapp_api.start_session():
                return True
        else:
            logger.error("Ошибка! Контейнер с внешним API не смог запустится.")
            raise Exception
    else:
        logger.info("Контейнер уже запущен, смотрим сессию")
        if requests_whatsapp_api.start_session():
            return True


def sending_bot(data: Applications, sellers: list[WholesaleCustomer]):
    association_li = []
    for seller in sellers:
        try:
            requests_whatsapp_api.sending_message(brand=data.motorcycle_brand,
                                                  model=data.motorcycle_model,
                                                  space_part=data.part_name_or_article,
                                                  phone_number=seller.whatsapp,
                                                  additional_info=data.additional_info)
        except Exception as exc:
            logger.error(f"Произошла ошибка с отправкой сообщения {exc}")
        association_li.append(seller)
        time.sleep(1)
    return association_li


def start_api(data: Applications, sellers: list[WholesaleCustomer]):
    start_container()
    logger.info("Всё успешно запустилось, начинаем рассылку!")
    time.sleep(2)
    return sending_bot(data=data, sellers=sellers)
