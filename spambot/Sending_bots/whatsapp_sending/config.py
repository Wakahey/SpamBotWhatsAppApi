BASE_URL = "http://localhost:3000/api"
BASE_HEADERS = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

type = "BMW"
model = "Cb-400"
space_part = 489234
BASE_MESSAGE = """Добрый день, мне нужны запчасти на мотоцикл
Марка: {}
Модель: {}
Запчасть: {}
{}"""
LIMIT_MESSAGE = 5
