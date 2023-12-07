# -*- coding: utf-8 -*-
BASE_URL = "http://localhost:3000/api"

BASE_HEADERS = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

BASE_MESSAGE = """Добрый день, мне нужны запчасти на мотоцикл
Марка: {}
Модель: {}
Год выпуска: {}
VIN номер: {}
Запчасть: {}
{}"""
LIMIT_MESSAGE = 5
