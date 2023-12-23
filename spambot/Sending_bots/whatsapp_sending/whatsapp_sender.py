# -*- coding: utf-8 -*-
from spambot.Sending_bots.whatsapp_sending.docker_run_api import (is_container_running,
                                                                  start_docker_container)
import time
from spambot.core.config import logger
import threading
from spambot.Sending_bots.whatsapp_sending import requests_whatsapp_api
from spambot.core.models.seller import WholesaleCustomer, Applications
from fastapi import HTTPException


def start_container():
    if requests_whatsapp_api.start_session():
        return True


def sending_bot(data: Applications, sellers: list[WholesaleCustomer]):
    association_li = []
    for seller in sellers:
        try:
            requests_whatsapp_api.sending_message(brand=data.motorcycle_brand,
                                                  model=data.motorcycle_model,
                                                  manufacturing_year=data.manufacturing_year,
                                                  vin_number=data.vin_number,
                                                  space_part=data.part_name_or_article,
                                                  phone_number=seller.whatsapp,
                                                  additional_info=data.additional_info)
            association_li.append(seller)
        except Exception as exc:
            logger.error(f"Произошла ошибка с отправкой сообщения {exc}")
        time.sleep(1)
    return association_li


def start_api(data: Applications, sellers: list[WholesaleCustomer]):
    start_container()
    logger.info("Всё успешно запустилось, начинаем рассылку!")
    time.sleep(2)
    return sending_bot(data=data, sellers=sellers)
