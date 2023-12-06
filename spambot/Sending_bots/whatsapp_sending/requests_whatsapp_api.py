import logging
import time
from spambot.Sending_bots.whatsapp_sending.config import BASE_URL, BASE_HEADERS, BASE_MESSAGE, LIMIT_MESSAGE
import requests
import json
from spambot.core.config import logger
from datetime import datetime


def start_session():
    if not get_status_sessions():
        logging.info("Начинается запуск сессии")
        url = f"{BASE_URL}/sessions/start"

        data = {
            "name": "default",
            "config": {
                "proxy": None,
                "webhooks": [
                    {
                        "url": "https://httpbin.org/post",
                        "events": ["message", "session.status"],
                        "hmac": None,
                        "retries": None,
                        "customHeaders": None
                    }
                ]
            }
        }
        data_json = json.dumps(data)
        try:
            response = requests.post(url=url,
                                     headers=BASE_HEADERS,
                                     data=data_json)
        except Exception as exc:
            logger.error(f"Ошибка с post запросом к запуску сессии {exc}")
            return False
        time.sleep(3)
    get_status_sessions()


def get_status_sessions():
    count = 0
    url = f"{BASE_URL}/sessions?all=true"
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            if json_data[0]["status"] == "STOPPED":
                logger.debug("Сессия не запущена")
                count += 1
                if count == 2:
                    return False
            elif json_data[0]["status"] == "STARTING":
                logger.debug("Сессия запускается, подождите")
            elif json_data[0]["status"] == "SCAN_QR_CODE":
                logger.info("Отсканируй QR CODE")
                time.sleep(4)
            elif json_data[0]["status"] == "WORKING":
                logger.info("Сессия запущена, QR код отсканирован")
                time.sleep(2)
                return True
            time.sleep(3)


def sending_message(brand, model, manufacturing_year, vin_number, space_part, additional_info, phone_number):
    url = f"{BASE_URL}/sendText"
    data = {
        "chatId": f"{phone_number}@c.us",
        "text": f"{BASE_MESSAGE.format(brand, model, manufacturing_year, vin_number, space_part, additional_info)}",
        "session": "default"
    }
    response = requests.post(url, headers=BASE_HEADERS, data=json.dumps(data))


def get_current_status():
    """
    Для получения статуса сессии на сайт
    :return:
    """
    url = f"{BASE_URL}/sessions?all=true"
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            if json_data[0]["status"] == "STOPPED":
                return "Сессия не запущена"
            elif json_data[0]["status"] == "STARTING":
                return "Сессия запускается, подождите"
            elif json_data[0]["status"] == "SCAN_QR_CODE":
                return "Отсканируй QR CODE"
            elif json_data[0]["status"] == "WORKING":
                return "Сессия запущена, QR код отсканирован"


def get_chat_messages(phone_number):
    ulr = f"""{BASE_URL}/messages?chatId={phone_number}%40c.us&downloadMedia=false&limit={LIMIT_MESSAGE}&session=default"""
    logger.info(f"Получаем чат с номером {phone_number}")
    response = requests.get(ulr)
    data_message = []
    if response.status_code == 200:
        json_data = response.json()
        print(json_data)
        for message in json_data:
            if message["fromMe"] is True:
                data_message.append({"name": "МотоДвиж",
                                     "body": message["body"],
                                     "time": datetime.fromtimestamp(message["timestamp"])
                                     })
            elif message["fromMe"] is False:
                data_message.append(
                    {"phone_number": (message["from"])[:11],
                     "body": message["body"],
                     "time": datetime.fromtimestamp(message["timestamp"])
                     })
    return data_message


def get_status_last_message_in_chat(phone_number):
    ulr = f"""{BASE_URL}/messages?chatId={phone_number}%40c.us&downloadMedia=false&limit=1&session=default"""
    logger.info(f"Получаем последнее сообщение с номером {phone_number}")
    response = requests.get(ulr)
    data_message = []
    if response.status_code == 200:
        json_data = response.json()
        if json_data[0]["fromMe"] is True:
            return False
        elif json_data[0]["fromMe"] is False:
            return json_data[0]["body"]


if __name__ == '__main__':
    # sending_message("BMW", "BBC4-000", "fsdfs")
    get_chat_messages(phone_number="79852988273")
