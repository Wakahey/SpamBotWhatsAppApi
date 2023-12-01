import time
from spambot.Sending_bots.whatsapp_sending.config import BASE_URL, BASE_HEADERS, BASE_MESSAGE
import requests
import json


def start_session():
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
    response = requests.post(url=url,
                             headers=BASE_HEADERS,
                             data=data_json)
    time.sleep(3)
    get_status_sessions()


def get_status_sessions():
    url = f"{BASE_URL}/sessions?all=true"
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            if json_data[0]["status"] == "STOPPED":
                print("Сессия не запущена")
            elif json_data[0]["status"] == "STARTING":
                print("Сессия запускается, подождите")
            elif json_data[0]["status"] == "SCAN_QR_CODE":
                print("Отсканируй QR CODE")
            elif json_data[0]["status"] == "WORKING":
                print("Сессия запущена, QR код отсканирован")
                break
            time.sleep(2)


def sending_message(type, model, space_part):
    url = f"{BASE_URL}/sendText"
    phone_number = 79166207979
    data = {
        "chatId": f"{phone_number}@c.us",
        "text": f"{BASE_MESSAGE.format(type, model, space_part)}",
        "session": "default"
    }
    response = requests.post(url, headers=BASE_HEADERS, data=json.dumps(data))
    

if __name__ == '__main__':
    sending_message("BMW", "BBC4-000", "fsdfs")
