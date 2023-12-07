# -*- coding: utf-8 -*-
from spambot.core.config import logger
from fastapi.exceptions import HTTPException
import docker
import keyboard
import threading
from docker.errors import NotFound, DockerException


def read_container_logs(container):
    try:
        for line in container.logs(stream=True, follow=True):
            print(line.decode('utf-8').strip())
    except Exception as e:
        logger.error(f"Ошибка при чтении логов контейнера: {e}")


def is_container_running(image_name):
    try:
        client = docker.from_env()
    except docker.errors.DockerException as exc:
        raise HTTPException(status_code=404, detail="Проблемы со сторонним приложением WhatsApp, сообщите айтишнику\n"
                                                    "(Docker контейнер не хочет запускаться, попробуйте запустить "
                                                    "вручную).")

    try:
        containers = client.containers.list(filters={'ancestor': image_name})
        return any(container.status == 'running' for container in containers)
    except docker.errors.NotFound:
        return False


def start_docker_container():
    """
    Старт докер контейнера с необходимым для работы
    whatsapp api, для автоматизированного отправления
    сообщений, запустить можно прям от сюда, снизу есть
    main

    """
    # Подключение к Docker API

    client = docker.from_env()

    # Название образа
    image_name = 'devlikeapro/whatsapp-http-api:latest'

    # Получение списка локальных образов
    local_images = client.images.list()

    # Проверка, существует ли образ локально
    image_exists = any(image.tags and image.tags[0] == image_name for image in local_images)

    # Если образа нет локально, скачиваем его
    if not image_exists:
        logger.debug(f"Образ {image_name} не найден локально. Загрузка образа...")
        client.images.pull(image_name)
        logger.info("Образ загружен успешно.")

    container_params = {
        'name': 'whatsapp-http-api',  # имя контейнера
        'remove': True,  # удаление контейнера после завершения
        'ports': {'3000/tcp': 3000},  # проброс порта 3000
        'detach': True,  # запуск в фоновом режиме
    }

    # Запуск контейнера с параметрами
    container = client.containers.run(image_name, **container_params)

    # Запуск потока для чтения вывода контейнера
    log_thread = threading.Thread(target=read_container_logs, args=(container,), daemon=True)
    log_thread.start()

    # Ожидание ввода пользователя
    logger.info("Для выключения контейнера нажмите клавишу 'Ctrl + Q'.")
    keyboard.wait("Ctrl + q")

    # Остановка контейнера
    logger.debug("Остановка контейнера...")
    container.stop()

    # Ожидание завершения потока
    log_thread.join(timeout=5)  # Подождать завершения потока в течение 5 секунд

    logger.debug("Контейнер остановлен.")


if __name__ == '__main__':
    start_docker_container()
