import docker
import keyboard
import threading


def read_container_logs(container):
    try:
        for line in container.logs(stream=True, follow=True):
            print(line.decode('utf-8').strip())
    except Exception as e:
        print(f"Ошибка при чтении логов контейнера: {e}")


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
    print(f"Образ {image_name} не найден локально. Загрузка образа...")
    client.images.pull(image_name)
    print("Образ загружен успешно.")

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
print("Для выключения контейнера нажмите клавишу 'Ctrl + Q'.")
keyboard.wait("Ctrl + q")

# Остановка контейнера
print("Остановка контейнера...")
container.stop()

# Ожидание завершения потока
log_thread.join(timeout=5)  # Подождать завершения потока в течение 5 секунд

print("Контейнер остановлен.")
